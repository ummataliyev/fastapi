from typing import Type
from typing import TypeVar
from typing import Generic

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

    def get_success_response(self, record: T, message: str = None) -> dict:
        """
        Standard success response for GET, POST, PATCH
        """
        return {
            "status": "success",
            "message": message or f"{self.model.__name__} fetched successfully",
            "data": self.to_dict(record)
        }

    def get_error_response(self, message: str = None) -> dict:
        """
        Standard error response with message and data fields
        """
        return {
            "status": "error",
            "message": message,
            "data": None,
        }

    def get_delete_success_response(self) -> dict:
        """
        Success response for DELETE
        """
        return {
            "status": "success",
            "message": f"{self.model.__name__} deleted successfully",
            "data": None
        }

    def get_create_success_response(self, record: T) -> dict:
        """
        Success response for POST (Create)
        """
        return {
            "status": "success",
            "message": f"{self.model.__name__} created successfully",
            "data": self.to_dict(record)
        }

    def get_update_success_response(self, record: T) -> dict:
        """
        Success response for PATCH (Update)
        """
        return {
            "status": "success",
            "message": f"{self.model.__name__} updated successfully",
            "data": self.to_dict(record)
        }
