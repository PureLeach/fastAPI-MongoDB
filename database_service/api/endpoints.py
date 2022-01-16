import shutil
import random
from typing import List

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

from . import services
from .schemas import FileSchema


router = APIRouter(prefix="/file", tags=["file"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_file(request: FileSchema = Depends(), file: UploadFile = File(...)):
    with open(f"data/{random.random()}.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {**request.dict(), "file_name": file.filename}


@router.get("/")
def get_all_files():
    response: List[dict] = services.get_all_files()
    return response


@router.get("/{id}")
def get_file(id: int):
    response: dict = services.get_file()
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_file(id: int, request: FileSchema):
    response: dict = services.update_file()
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(id: int):
    response: dict = services.delete_file()
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="File not found")
