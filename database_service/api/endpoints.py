from typing import List
import shutil
from datetime import datetime, time, timedelta
import random
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Request,
    HTTPException,
    UploadFile,
    File,
)

from .schemas import FileSchema


router = APIRouter(prefix="/file", tags=["file"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_file(request: FileSchema = Depends(), file: UploadFile = File(...)):
    with open(f"data/{random.random()}.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {**request.dict(), "file_name": file.filename}


@router.get("/")
def get_all_files():
    return "Read all files"


@router.get("/{id}")
def get_file(id: int, response: Response):
    if id < 5:
        return f"Read one file {id}"
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_file(id: int, request: FileSchema):
    return request


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(id: int):
    return f"Delete file {id}"
