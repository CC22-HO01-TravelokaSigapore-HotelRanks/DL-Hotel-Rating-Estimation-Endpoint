# For API stuff
from fastapi import APIRouter, Response, Request, status
# from pydantic import BaseModel
from fastapi_redis_cache import cache
from modules.functions import *

api_router = APIRouter()

# class Position(BaseModel):
#     longitude:float
#     latitude:float

@api_router.post("/for-you/")
@cache()
async def for_you(request:Request, response:Response):
    json_req = await request.json()
    print(json_req["user_id"])
    print(json_req["longitude"])
    print(json_req["latitude"])
    return "BRUH"