import os

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv


load_dotenv("back.env")

client: MongoClient = MongoClient(
    host=os.getenv("MONGO_HOST", "localhost"),
    port=int(os.getenv("MONGO_PORT", 27017)),
    username=os.getenv("MONGO_USER", "root"),
    password=os.getenv("MONGO_PASSWORD", "rootpassword"),
    serverSelectionTimeoutMS=10,
    connectTimeoutMS=20000,
)

try:
    info: dict = client.server_info()
except ServerSelectionTimeoutError:
    print("server is down!!!!")

db: object = client["My_test_db"]
collection: object = db["test-collection"]
