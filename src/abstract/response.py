"""
Base class for routers response
"""
from typing import List
from typing import Type
from typing import Generic
from typing import TypeVar

from src.abstract.scheme import BaseScheme

T = TypeVar('T')


class BaseResponse(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def to_dict(self, record: T) -> dict:
        """
        Convert model to dictionary for API response
        """
        if hasattr(record, "dict"):
            return record.dict()
        return record.__dict__

    def get_success_response(self, record: T, message: str = None) -> BaseScheme:
        """
        Standard success response for GET, POST, PATCH
        """
        return BaseScheme(
            status="success",
            message=message or f"{self.model.__name__} fetched successfully",
            data=self.to_dict(record)
        )

    def get_error_response(self, message: str = None) -> BaseScheme:
        """
        Standard error response with message and data fields
        """
        return BaseScheme(
            status="error",
            message=message or "An unexpected error occurred",
            data=None
        )

    def get_delete_success_response(self) -> BaseScheme:
        """
        Success response for DELETE
        """
        return BaseScheme(
            status="success",
            message=f"{self.model.__name__} deleted successfully",
            data=None
        )

    def get_create_success_response(self, record: T) -> BaseScheme:
        """
        Success response for POST (Create)
        """
        return BaseScheme(
            status="success",
            message=f"{self.model.__name__} created successfully",
            data=self.to_dict(record)
        )

    def get_update_success_response(self, record: T) -> BaseScheme:
        """
        Success response for PATCH (Update)
        """
        return BaseScheme(
            status="success",
            message=f"{self.model.__name__} updated successfully",
            data=self.to_dict(record)
        )

    def get_all_response(self, records: List[T], message: str = None) -> BaseScheme:
        """
        Success response for retrieving all records (GET list)
        """
        return BaseScheme(
            status="success",
            message=message or f"All {self.model.__name__}s fetched successfully",
            data=[self.to_dict(record) for record in records]
        )
