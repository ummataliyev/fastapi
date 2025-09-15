"""
Base class for routers response scheme
"""

from typing import TypeVar
from typing import Generic

from pydantic import BaseModel


T = TypeVar("T")


class BaseScheme(BaseModel, Generic[T]):
    status: str
    message: str
    data: T | None = None
