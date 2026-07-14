from pydantic import BaseModel
from typing import Optional


class Error(BaseModel):
    message: str
    code: Optional[str]
    description: Optional[str]
    