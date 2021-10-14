import json
from pymongo import MongoClient

from sample.config import APP_MONGO_URL, APP_MONGO_USER_COL

db = MongoClient(APP_MONGO_URL).get_default_database()


def setup_initial_data():
    user_col = db.create_collection(APP_MONGO_USER_COL)
    with open("users.json", "r") as f:
        user_col.insert_many(json.load(f))

def teardown_database():
    db[APP_MONGO_USER_COL].drop()
