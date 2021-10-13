from pymongo import MongoClient
from sample_app.config import APP_MONGO_URL

_client = MongoClient(APP_MONGO_URL).get_default_database()

def setup_mongo():
    _client.create_collection("users")
