import os
from pymongo import MongoClient

MONGO_URI = os.environ["MONGO_URI"]
MONGO_DBNAME = os.environ["MONGO_DBNAME"]

client = MongoClient(MONGO_URI)
mongodb = client[MONGO_DBNAME]

