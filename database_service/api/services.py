from datetime import datetime
import shutil
from typing import List, Optional
import pathlib
from bson.objectid import ObjectId
from bson.errors import InvalidId
from uuid import uuid4


from fastapi import UploadFile, HTTPException, status

from core.settings import collection, logger


def save_file(file: UploadFile) -> dict:
    try:
        file_uuid: str = str(uuid4())
        file_extension: str = pathlib.Path(file.filename).suffix
        file_path: str = f"data/{file_uuid + file_extension}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_metadata: dict = {
            "file_uuid": file_uuid,
            "file_name": file.filename,
            "file_path": file_path,
            "upload_time": datetime.utcnow(),
            "user_id": str(uuid4()),
        }
        return file_metadata
    except Exception as e:
        logger.error(f"Error saving the file to disk: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving the file to disk",
        )


def post_file(file_data: dict) -> str:
    try:
        _id: ObjectId = collection.insert_one(file_data.copy()).inserted_id
        return str(_id)
    except Exception as e:
        logger.error(f"Error writing data to mongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error writing data to mongoDB",
        )


def get_all_files() -> List[dict]:
    try:
        files: list = []
        for file in collection.find({}):
            file["id"] = str(file["_id"])
            del file["_id"]
            files.append(file)
        return files
    except Exception as e:
        logger.error(f"Error getting data from mongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting data from mongoDB",
        )


def get_file(id: str) -> dict:
    try:
        file: Optional[dict] = collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not a valid ObjectId",
        )
    except Exception as e:
        logger.error(f"Error getting data from mongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting data from mongoDB",
        )
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    else:
        file["id"] = str(file["_id"])
        del file["_id"]
        return file


def update_file(id: str, file_data: dict) -> dict:
    try:
        file_data: Optional[dict] = collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": file_data}
        )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not a valid ObjectId",
        )
    except Exception as e:
        logger.error(f"Error updating data from mongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating data from mongoDB",
        )
    if file_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )


def delete_file(id: str) -> bool:
    pass
