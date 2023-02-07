import sys
from pathlib import Path

from environs import Env
from loguru import logger
from pymongo import MongoClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

env = Env()
env.read_env(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent


SERVER_HOST = env.str('SERVER_HOST', default='0.0.0.0')
SERVER_PORT = env.int('SERVER_PORT', default=8000)
SERVER_RELOAD = env.bool('SERVER_RELOAD', default=True)

# Setting up the logger
logger.remove()

# Format of logs to a file
logger.add(
    'logs/backend.log',
    format='{time:DD/MM/YYYY HH:mm:ss} | {name}:{function}:{line} | {level} | {message}',
    level='DEBUG',
    rotation='10 MB',
    serialize=True,
    compression='zip',
    backtrace=True,
    diagnose=True,
    encoding='utf-8',
)

# Format of logs to the terminal
logger.add(
    sys.stdout,
    format='<green>{time:DD/MM/YYYY HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>',
    level='DEBUG',
    backtrace=True,
    diagnose=True,
    colorize=True,
)

MONGO_USER = env.str('MONGO_USER')
MONGO_PASSWORD = env.str('MONGO_PASSWORD')
MONGO_HOST = env.str('MONGO_HOST', default='127.0.0.1')
MONGO_PORT = env.int('MONGO_PORT', default=27017)
MONGO_DB = env.str('MONGO_DB', default='service')
MONGO_COLLECTION = env.str('MONGO_COLLECTION', default='files')
MONGO_TIMEOUT_MS = env.int('MONGO_TIMEOUT_MS', default=10000)

# Connecting to MongoDB
client: MongoClient = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    serverSelectionTimeoutMS=MONGO_TIMEOUT_MS,
    connectTimeoutMS=MONGO_TIMEOUT_MS,
)

try:
    info: dict = client.server_info()
except (ServerSelectionTimeoutError, OperationFailure) as e:
    logger.error(f'Connection error to MongoDB: {e}')

db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
