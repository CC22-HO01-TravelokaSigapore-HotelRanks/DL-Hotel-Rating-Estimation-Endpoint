# Dotenv if available
print("INFO: Loading dotenv if available")
from dotenv import load_dotenv
load_dotenv()

# Init Database
print("INFO: Testing Database")
from modules.database import db

# Init Redis
print("INFO: Connecting to redis")
from modules.redis import create_key, redis
if not redis.ping():
    print("ERROR: Cannot connect to REDIS")
print("INFO: Redis connected ")

# Init API
import uvicorn
from fastapi import FastAPI
api = FastAPI()

# Include API
from modules.api import api_router
api.include_router(api_router)

# Init Endpoint
port = 8001
print(f"Listening to http://0.0.0.0:{port}")
uvicorn.run(api, host='0.0.0.0',port=port)