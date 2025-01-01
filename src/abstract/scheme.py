from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    status: str
    message: str
    data: Any
