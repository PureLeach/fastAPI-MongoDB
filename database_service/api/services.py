import os
import pathlib
import shutil
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from bson.errors import InvalidId
from bson.objectid import ObjectId
from fastapi import HTTPException, UploadFile, status

from core.settings import BASE_DIR, collection, logger


def save_file(file: UploadFile) -> dict:
    """
    Saving a file on disk and generating metadata about it

    Args:
        file (UploadFile): File data

    Raises:
        HTTPException: Error saving the file to disk

    Returns:
        dict: Metadata about the file
    """
    try:
        file_uuid: str = str(uuid4())
        file_extension: str = pathlib.Path(file.filename).suffix
        file_path: str = f'data/{file_uuid + file_extension}'
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_metadata: dict = {
            'file_uuid': file_uuid,
            'file_name': file.filename,
            'file_path': file_path,
            'upload_time': datetime.utcnow(),
            'user_id': str(uuid4()),
        }
        return file_metadata
    except Exception as e:
        logger.error(f'Error saving the file to disk: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error saving the file to disk',
        )


def create_file(file_data: dict) -> str:
    """
    Saving file data to a database

    Args:
        file_data (dict): Data about the file

    Raises:
        HTTPException: Error writing data to MongoDB

    Returns:
        str: File id in MongoDB
    """
    try:
        _id: ObjectId = collection.insert_one(file_data.copy()).inserted_id
        return str(_id)
    except Exception as e:
        logger.error(f'Error writing data to MongoDB: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error writing data to MongoDB',
        )


def get_all_files() -> List[dict]:
    """
    Getting information about all files saved in the database

    Raises:
        HTTPException: Error getting data from MongoDB

    Returns:
        List[dict]: Files data
    """
    try:
        files: list = []
        for file in collection.find({}):
            file['id'] = str(file['_id'])
            del file['_id']
            files.append(file)
        return files
    except Exception as e:
        logger.error(f'Error getting data from MongoDB: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error getting data from MongoDB',
        )


def get_file(id: str) -> dict:
    """
    Getting information about one file by its id

    Args:
        id (str): File id in MongoDB

    Raises:
        HTTPException: Not a valid ObjectId
        HTTPException: Error getting data from MongoDB
        HTTPException: File not found

    Returns:
        dict: File data
    """
    try:
        file: Optional[dict] = collection.find_one({'_id': ObjectId(id)})
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not a valid ObjectId',
        )
    except Exception as e:
        logger.error(f'Error getting data from MongoDB: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error getting data from MongoDB',
        )
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )
    else:
        file['id'] = str(file['_id'])
        del file['_id']
        return file


def update_file(id: str, data: dict) -> None:
    """
    Updating information about a file by its id

    Args:
        id (str): File id in MongoDB
        file_data (dict): New data about the file

    Raises:
        HTTPException: Not a valid ObjectId
        HTTPException: Error updating data from MongoDB
        HTTPException: File not found
    """
    try:
        file_data: Optional[dict] = collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': data})
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not a valid ObjectId',
        )
    except Exception as e:
        logger.error(f'Error updating data from MongoDB: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error updating data from MongoDB',
        )
    if file_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )


def delete_file(id: str) -> None:
    """
    Deleting information about a file by its id

    Args:
        id (str): File id in MongoDB

    Raises:
        HTTPException: Not a valid ObjectId
        HTTPException: Error deleting data from MongoDB
        HTTPException: File not found
    """
    try:
        file_data: Optional[dict] = collection.find_one_and_delete({'_id': ObjectId(id)})
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not a valid ObjectId',
        )
    except Exception as e:
        logger.error(f'Error deleting data from MongoDB: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error deleting data from MongoDB',
        )
    if file_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )
    else:
        delete_file_from_disk(file_data['file_path'])


def delete_file_from_disk(file_path: str) -> None:
    """
    Deleting a file from the file system

    Args:
        file_path (str): Relative path to the file
    """
    if os.path.isfile(os.path.join(BASE_DIR, file_path)):
        os.remove(os.path.join(BASE_DIR, file_path))
    else:
        logger.error(f'File "{file_path}" doesn`t exists')
