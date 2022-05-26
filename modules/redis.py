import redis as r
import os

def create_key(user_id):
    return f"user-id-{user_id}"

def list_to_dict(list):
    return {"list" : list}

def dict_to_list(dict):
    return dict["list"]

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
con_str = os.getenv("REDIS_CON_STRING")

pool = r.ConnectionPool(host=host, port=port, db=0)
redis = r.Redis(connection_pool=pool)
