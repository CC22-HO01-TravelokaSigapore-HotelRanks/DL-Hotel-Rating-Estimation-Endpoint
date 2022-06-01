# For API stuff
from fastapi import APIRouter, Response, Request, status
from modules.functions import *
from modules.models import *

import numpy as np
import tensorflow as tf

import traceback

# Redis thingy
from modules.redis import *

api_router = APIRouter()

@api_router.get("/")
async def hello_world():
    return "Hello from for you page endpoint"

@api_router.post("/")
async def for_you(request:Request, response:Response):
    try:
        NUM_RECS = 10
        MINIMUM_REVIEWS = 10
        
        json_req = await request.json()

        longitude = json_req["longitude"]
        latitude = json_req["latitude"]
        user_id = json_req["user_id"]
        key = create_key(user_id)
        
        # Search for a key in redis, if not found or expire continue
        byte_json = redis.get(key)
        if byte_json is not None:
            print(f"INFO: '{key}' cached in redis")
            final_list = string_to_list(byte_json.decode())
            return final_list
        print(f"INFO: '{key}' not cached in redis")
        
        # Do pipelines
        # Check if the user is already have the review enough to "train" the model (10 reviews minimum)
        df_review = user_enough_review(MINIMUM_REVIEWS, user_id)
        if df_review is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message" : "Not enough review to train user models"}
        
        df_hotel = db.hotel()
        df_hotel_attr = df_hotel.filter(items=hotel_train_items).copy()
        df_user = db.user()
        user_attr, hotel_attr, rating = create_training_data(df_review, 
                                                        df_hotel_attr, df_user)
        non_original_model = create_model() 
        non_original_model.set_weights(model.get_weights())
        non_original_model.compile(optimizer="adam", loss="mean_absolute_error", metrics=["mean_absolute_error"])
        non_original_model.fit([user_attr, hotel_attr], rating, epochs=10, verbose=0)
        
        # Get 10 closest hotel user
        # Predict those 10 closest hotel based on user models
        hotel_predict_ids = closest_hotel_id(NUM_RECS, longitude, latitude, df_hotel)
        hotel_predict = df_hotel_attr.loc[hotel_predict_ids].values
        hotel_predict = tf.convert_to_tensor(hotel_predict)
        user_predict = tf.convert_to_tensor([user_attr[0] for _ in range(NUM_RECS)])
        prediction = non_original_model.predict([user_predict, hotel_predict])
        prediction = prediction.reshape(1, -1)[0]
        prediction = np.argsort(prediction)[::-1]
        
        final_recs = []
        for i in prediction:
            final_recs.append(int(hotel_predict_ids[i]))
        
        # Save to redis
        print(f"INFO: '{key}' saved in redis")
        redis.set(key,list_to_string(final_recs), ex=60)
        
        return final_recs
    except:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message" : "Internal server error"}