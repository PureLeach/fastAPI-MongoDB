from datetime import datetime

from pydantic import BaseModel


class FileRequest(BaseModel):
    author: str
    description: str


class FileResponse(FileRequest):
    id: str
    file_uuid: str
    file_name: str
    file_path: str
    upload_time: datetime
    user_id: str
