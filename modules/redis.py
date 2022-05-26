import redis as r
import os
from ast import literal_eval

def create_key(user_id):
    return f"user-id-{user_id}"

def list_to_string(list):
    return str(list)

def string_to_list(string):
    return literal_eval(string)

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
con_str = os.getenv("REDIS_CON_STRING")

pool = r.ConnectionPool(host=host, port=port, db=0)
redis = r.Redis(connection_pool=pool)
