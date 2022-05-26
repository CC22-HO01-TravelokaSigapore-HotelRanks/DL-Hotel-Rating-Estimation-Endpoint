# For API stuff
from fastapi import APIRouter, Response, Request, status
from modules.functions import *

# Redis thingy
from redis.commands.json.path import Path
from modules.redis import create_key, dict_to_list, list_to_dict, redis

api_router = APIRouter()

def dummy_pipelines():
    return [1,2,3,4]

@api_router.post("/")
async def for_you(request:Request, response:Response):
    json_req = await request.json()

    longitdue = json_req["longitude"]
    latitude = json_req["latitude"]
    user_id = json_req["user_id"]
    key = create_key(user_id)
    
    # Search for a key in redis, if not found or expire continue
    redis_json = redis.json().get(key)
    if redis_json is not None:
        print(f"INFO: '{key}' cached in redis")
        final_list = dict_to_list(redis_json)
        return final_list
    print(f"INFO: '{key}' not cached in redis")
    
    # Do pipelines
    final_list = dummy_pipelines()
    
    # Save to redis
    print(f"INFO: '{key}' saved in redis")
    redis.json().set(key, Path.root_path(),list_to_dict(final_list))
    redis.expire(key, 60)
    
    return final_list