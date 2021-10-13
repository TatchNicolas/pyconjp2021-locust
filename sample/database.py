import json
from pymongo import MongoClient

from sample.config import APP_MONGO_URL

db = MongoClient(APP_MONGO_URL).get_default_database()

def setup():
    user_col = db.create_collection("users")
    with open("users.json", "r") as f:
        user_col.insert_many(json.load(f))
