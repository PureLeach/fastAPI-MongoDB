from typing import List, Optional

from pydantic import BaseModel


class FileSchema(BaseModel):
  name: str
  author: str
  content: str