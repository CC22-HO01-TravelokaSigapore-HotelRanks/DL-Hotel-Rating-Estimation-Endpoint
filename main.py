# Dotenv if available
print("INFO: Loading dotenv if available")
from dotenv import load_dotenv
load_dotenv()

# For Database Caching
print("INFO: Testing Database")
from modules.database import db

# For API
import uvicorn
from fastapi import FastAPI, Request, Response
# Instantiate API
api = FastAPI()

# Init Redis
import os
from fastapi_redis_cache import FastApiRedisCache, cache
@api.on_event("startup")
def startup():
    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT")
    con_str = os.getenv("REDIS_CON_STRING")
    
    final_redis_str = "redis://"
    if con_str is not None:
        final_redis_str += con_str
    else:
        final_redis_str += f"{host}:{port}"
    
    print("INFO: Init Redis")
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", final_redis_str),
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response]
    )
    
# Init API
from modules.api import api_router
api.include_router(api_router)

# Init Endpoint
port = 8001
print(f"Listening to http://0.0.0.0:{port}")
uvicorn.run(api, host='0.0.0.0',port=port)