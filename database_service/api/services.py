from lib2to3.pgen2.token import OP
import shutil
from typing import List, Optional
import pathlib
from bson.objectid import ObjectId
from uuid import UUID, uuid4
import random
import datetime

from fastapi import UploadFile, HTTPException, status

from core.settings import collection, logger


def save_file(file: UploadFile) -> dict:
    try:
        file_uuid: str = str(uuid4())
        file_extension: str = pathlib.Path(file.filename).suffix
        file_path: str = f"data/{file_uuid + file_extension}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_info: dict = {"file_uuid": file_uuid, "file_name": file.filename, "file_path": file_path, "user_id": str(uuid4())}
        return file_info
    except Exception as e:
        logger.error(f"Error saving the file to disk: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving the file to disk")
    

def post_file(file_data: dict) -> str:
    file_id: ObjectId  = collection.insert_one(file_data).inserted_id
    return str(file_id)


def get_all_files() -> List[dict]:
    pass


def get_file(id: str) -> dict:
    pass


def update_file(id: str) -> dict:
    pass


def delete_file(id: str) -> bool:
    pass
