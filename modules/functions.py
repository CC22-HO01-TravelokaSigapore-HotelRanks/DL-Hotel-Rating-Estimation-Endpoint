from typing import Union
import pandas as pd
import tensorflow as tf
import haversine as hs
import numpy as np

def user_enough_review(minimum_reviews:int, user_id: int, df: pd.DataFrame) -> Union[pd.DataFrame, None]:
  """
  Get Users Reviews. If less than minimum_reviews returns 0. 
  If not will return the reviews dataframe contains user_id, hotel_id, rating
  """
  df_temp = df[df["user_id"] == user_id]
  if len(df_temp) < minimum_reviews:
    return None
  return df_temp

def create_training_data(training_review, df_hotel, df_user):
  """
  training_review : dataframe[hotel_id, user_id, rating]
  df_hotel : dataframe["hotel attributes"] -> must have 14 attr
  df_user : dataframe["user attributes"] -> must have 4 attr

  Create Training tensor based on hotel_id, user_id lookups to hotel dataframe
  and user dataframe as feature and targets a rating in training_review dataframe
  """
  user_attr = []
  hotel_attr = []
  rating = []

  for _, row in training_review.iterrows():
    hotel_id = row["hotel_id"]
    user_id = row["user_id"]
    rating.append(row["rating"])
    user_attr.append(df_user.loc[user_id].values)
    hotel_attr.append(df_hotel.loc[hotel_id].values)

  user_attr = tf.convert_to_tensor(user_attr)
  hotel_attr = tf.convert_to_tensor(hotel_attr)
  rating = tf.convert_to_tensor(rating)

  return user_attr, hotel_attr, rating

def closest_hotel_id(num: int, longitude, latitude, df_hotel_in) -> np.ndarray:
  """
  df_hotel_in : dataframe[longitude, latitude]
  Gives (num) hotel ids based on longitude and latitude inputs
  """
  df_hotel = df_hotel_in.copy()
  user = (latitude, longitude)
  df_hotel["coordinate"] = list(zip(df_hotel["latitude"], df_hotel["longitude"]))
  df_hotel["distance_to_user"] = df_hotel["coordinate"].apply(lambda x: hs.haversine(user, x))
  df_hotel = df_hotel.sort_values(by=["distance_to_user"])
  return df_hotel.head(num).index.values