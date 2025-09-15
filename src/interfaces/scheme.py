"""
Base class for routers response scheme
"""

from typing import TypeVar
from typing import Generic

from pydantic import BaseModel


T = TypeVar("T")


class BaseScheme(BaseModel, Generic[T]):
    """
    Generic Pydantic schema for API responses.

    Provides a standardized structure for all API responses with the following fields:

    Attributes:
        status (str): The status of the response, e.g., "success" or "error".
        message (str): A human-readable message describing the response.
        data (T | None): Optional payload containing the response data. Can be of any type.
    """
    status: str
    message: str
    data: T | None = None
