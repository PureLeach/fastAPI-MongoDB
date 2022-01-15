from typing import List

from fastapi import APIRouter, Depends

from .schemas import FileBase
# from sqlalchemy.orm import Session
# from db.database import get_db
# from db import db_user


router = APIRouter(
  prefix='/file',
  tags=['file']
)


# Create file
@router.post('/', response_model=FileBase)
def create_file(request: FileBase):
    return "Create file"
#   return db_user.create_user(db, request)


# Read all files
@router.get('/', response_model=List[FileBase])
def get_all_files():
    return "Read all files"
#   return db_user.get_all_users(db)


# Read one file
@router.get('/{id}', response_model=FileBase)
def get_file(id: int):
    return f"Read one file {id}"
#   return db_user.get_user(db, id)


# Update file
@router.put('/{id}')
def update_file(id: int, request: FileBase):
    return f"Update file {id}"
#   return db_user.update_user(db, id, request)


# Delete file
@router.delete('/{id}')
def delete_file(id: int):
    return f"Delete file {id}"
#   return db_user.delete_user(db, id)
