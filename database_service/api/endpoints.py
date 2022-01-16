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
from .schemas import FileRequest, FileResponse


router = APIRouter(prefix="/file", tags=["file"])


@router.post("/", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
def create_file(request: FileRequest = Depends(), file: UploadFile = File(...)):
    file_metadata: dict = services.save_file(file)
    file_data: dict = {**request.dict(), **file_metadata}
    file_id: str = services.post_file(file_data)
    return {"id": file_id, **file_data}


@router.get("/", response_model=List[FileResponse])
def get_all_files():
    files_data: List[dict] = services.get_all_files()
    return files_data


@router.get("/{id}", response_model=FileResponse)
def get_file(id: str):
    file_data: dict = services.get_file(id)
    return file_data


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_file(id: str, request: FileRequest):
    response: dict = services.update_file()
    if response:
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(id: str):
    response: dict = services.delete_file()
    if response:
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
