"""
Initialize interfaces
"""

from .interface import IRepository
from .repository import BaseRepository
from .response import BaseResponse
from .scheme import BaseScheme
from .service import BaseService

__all__ = [
    "IRepository",
    "BaseRepository",
    "BaseResponse",
    "BaseScheme",
    "BaseService",
]
