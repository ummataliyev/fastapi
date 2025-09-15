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
    """
    Generic response builder for API endpoints.

    Provides standardized success and error responses for any model type `T`.
    Converts model instances to dictionaries and formats responses using BaseScheme.
    """

    def __init__(self, model: Type[T]):
        """
        Initialize the response builder with a model type.

        :param model: The model class for which responses will be generated.
        """
        self.model = model

    def to_dict(self, record: T) -> dict:
        """
        Convert a model instance to a dictionary suitable for API responses.

        :param record: Model instance to convert.
        :return: Dictionary representation of the model.
        """
        if hasattr(record, "dict") and callable(record.dict):
            return record.dict()
        return record.__dict__

    def _build_response(
        self,
        status: str,
        message: str,
        data: Union[dict, List[dict], None] = None
    ) -> "BaseScheme":
        """
        Internal helper to standardize response construction.

        :param status: Response status, e.g., "success" or "error".
        :param message: Response message describing the operation result.
        :param data: Optional payload data (dict, list of dicts, or None).
        :return: Standardized BaseScheme response instance.
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
    ) -> "BaseScheme":
        """
        Generate a standardized success response.

        :param record: Single model instance or list of instances to include in response.
        :param message: Optional custom message; if not provided, a default is generated.
        :param action: Optional action context, e.g., "create", "update", or "delete".
        :return: BaseScheme response with status "success".
        """
        msg = message or self._default_message(record, action)
        if isinstance(record, list):
            data = [self.to_dict(r) for r in record]
        elif record is not None:
            data = self.to_dict(record)
        else:
            data = None
        return self._build_response("success", msg, data)

    def error(self, message: str = None) -> "BaseScheme":
        """
        Generate a standardized error response.

        :param message: Optional error message; defaults to a generic message.
        :return: BaseScheme response with status "error".
        """
        return self._build_response(
            status="error",
            message=message or "An unexpected error occurred",
            data=None
        )

    def _default_message(self, record: Union[T, List[T], None], action: str) -> str:
        """
        Generate default messages based on the action and type of record.

        :param record: Single model instance, list of instances, or None.
        :param action: Action being performed: "create", "update", "delete", or None.
        :return: A descriptive default message string.
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
        return "Operation completed successfully"

    def get_success_response(self, record: T, message: str = None) -> "BaseScheme":
        """
        Return a generic success response for a single record.

        :param record: Model instance to include in the response.
        :param message: Optional custom message.
        :return: BaseScheme success response.
        """
        return self.success(record=record, message=message, action=None)

    def get_create_success_response(self, record: T) -> "BaseScheme":
        """
        Return a success response for a create action.

        :param record: Model instance that was created.
        :return: BaseScheme success response with "create" context.
        """
        return self.success(record=record, action="create")

    def get_update_success_response(self, record: T) -> "BaseScheme":
        """
        Return a success response for an update action.

        :param record: Model instance that was updated.
        :return: BaseScheme success response with "update" context.
        """
        return self.success(record=record, action="update")

    def get_delete_success_response(self) -> "BaseScheme":
        """
        Return a success response for a delete action.

        :return: BaseScheme success response with "delete" context.
        """
        return self.success(record=None, action="delete")

    def get_all_response(self, records: List[T], message: str = None) -> "BaseScheme":
        """
        Return a success response for fetching multiple records.

        :param records: List of model instances to include in response.
        :param message: Optional custom message.
        :return: BaseScheme success response.
        """
        return self.success(record=records, message=message)
