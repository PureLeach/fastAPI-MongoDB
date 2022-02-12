import os
from pathlib import Path
import sys

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from environs import Env
from loguru import logger
import yaml


BASE_DIR: object = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(override=True)

with open(os.path.join(BASE_DIR, "core/settings.yaml")) as f:
    settings: dict = yaml.safe_load(f)[os.getenv('OS_SHELL', 'docker')]


# Setting up the logger
log_settings: dict = settings["logs"]
logger.remove()

# Format of logs to a file
logger.add(
    log_settings["directory"],
    format=log_settings["format"],
    level=log_settings["level"],
    rotation=log_settings["rotation"],
    compression=log_settings["compression"],
    backtrace=log_settings["backtrace"],
    diagnose=log_settings["diagnose"],
    encoding=log_settings["encoding"],
)

# Format of logs to the terminal
logger.add(
    sys.stdout,
    format=log_settings["format_terminal"],
    level=log_settings["level"],
    backtrace=log_settings["backtrace"],
    diagnose=log_settings["diagnose"],
    colorize=True,
)


# Connecting to MongoDB
mongo_settings: dict = settings["mongoDB"]
client: MongoClient = MongoClient(
    host=mongo_settings["host"],
    port=mongo_settings["port"],
    username=os.getenv("MONGO_USER", "root"),
    password=os.getenv("MONGO_PASSWORD", "rootpassword"),
    serverSelectionTimeoutMS=mongo_settings["serverSelectionTimeoutMS"],
    connectTimeoutMS=mongo_settings["connectTimeoutMS"],
)

try:
    info: dict = client.server_info()
except (ServerSelectionTimeoutError, OperationFailure) as e:
    logger.error(f"Connection error to MongoDB: {e}")

db: object = client[mongo_settings["db"]]
collection: object = db[mongo_settings["collection"]]
