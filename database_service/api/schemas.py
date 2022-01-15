from pydantic import BaseModel


class FileBase(BaseModel):
  name: str
