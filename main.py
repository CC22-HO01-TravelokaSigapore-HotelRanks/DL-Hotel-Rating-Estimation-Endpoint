# Dotenv if available
print("INFO: Loading dotenv if available")
from dotenv import load_dotenv
load_dotenv()

# Init Deep Learning Models
print("INFO: Load Models Deep Learning Models")
from modules.models import model
print("INFO: Deep Learning Models Loaded")

# Init Database
print("INFO: Testing Database")
from modules.database import db

# Init Redis
print("INFO: Connecting to Redis")
from modules.redis import redis
if not redis.ping():
    print("ERROR: Cannot connect to REDIS")
    exit(1)
print("INFO: Redis connected ")

# Scheduling for Database Caching
print("INFO: Loading scheduler")
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(db.cache_database, 'interval', minutes=2)
scheduler.start()

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