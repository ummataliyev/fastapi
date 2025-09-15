"""
Base class for routers response
"""

from typing import List
from typing import Type
from typing import Union
from typing import Generic
from typing import TypeVar

from src.interfaces.scheme import BaseScheme


T = TypeVar("T")


class BaseResponse(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def to_dict(self, record: T) -> dict:
        """
        Convert model instance to dictionary for API response
        """
        if hasattr(record, "dict") and callable(record.dict):
            return record.dict()
        return record.__dict__

    def _build_response(
        self,
        status: str,
        message: str,
        data: Union[dict, List[dict], None] = None
    ) -> BaseScheme:
        """
        Internal helper to standardize response building
        """
        return BaseScheme(
            status=status,
            message=message,
            data=data
        )

    def success(
        self,
        record: Union[T, List[T], None] = None,
        message: str = None,
        action: str = None
    ) -> BaseScheme:
        """
        Generic success response
        """
        msg = message or self._default_message(record, action)
        if isinstance(record, list):
            data = [self.to_dict(r) for r in record]
        elif record is not None:
            data = self.to_dict(record)
        else:
            data = None
        return self._build_response("success", msg, data)

    def error(self, message: str = None) -> BaseScheme:
        """
        Standard error response
        """
        return self._build_response(
            status="error",
            message=message or "An unexpected error occurred",
            data=None
        )

    def _default_message(self, record: Union[T, List[T], None], action: str) -> str:
        """
        Generate default messages based on action and record
        """
        name = self.model.__name__
        if action == "create":
            return f"{name} created successfully"
        elif action == "update":
            return f"{name} updated successfully"
        elif action == "delete":
            return f"{name} deleted successfully"
        elif isinstance(record, list):
            return f"All {name}s fetched successfully"
        elif record is not None:
            return f"{name} fetched successfully"
        return f"Operation completed successfully"

    # Convenience methods
    def get_success_response(self, record: T, message: str = None) -> BaseScheme:
        return self.success(record=record, message=message, action=None)

    def get_create_success_response(self, record: T) -> BaseScheme:
        return self.success(record=record, action="create")

    def get_update_success_response(self, record: T) -> BaseScheme:
        return self.success(record=record, action="update")

    def get_delete_success_response(self) -> BaseScheme:
        return self.success(record=None, action="delete")

    def get_all_response(self, records: List[T], message: str = None) -> BaseScheme:
        return self.success(record=records, message=message)
