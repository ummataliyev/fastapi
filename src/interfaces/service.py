"""
Base service class for interacting with repositories
"""

from typing import List
from typing import Type
from typing import TypeVar
from typing import Generic

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.interfaces.repository import BaseRepository

from db.storage.postgres import get_db

T = TypeVar("T")


class BaseService(Generic[T]):
    """
    Generic service layer providing standard CRUD operations.

    Wraps a BaseRepository to perform database operations for a specific model type `T`.
    Designed to be inherited by concrete service classes for specific entities.
    """

    def __init__(self, db_session: AsyncSession, model: Type[T]):
        """
        Initialize the BaseService with a database session and model.

        :param db_session: Async SQLAlchemy session for database access.
        :param model: SQLAlchemy model class representing the entity.
        """
        self.repository = BaseRepository[T](db_session, model)

    async def get_by_id(self, record_id: int) -> T:
        """
        Retrieve a record by its primary key ID.

        :param record_id: ID of the record to fetch.
        :return: Model instance if found.
        :raises ValueError: If the record is not found.
        """
        record = await self.repository.get(id=record_id)
        if record is None:
            raise ValueError(f"{self.repository.model.__name__} with id {record_id} not found")
        return record

    async def get_all(
        self, skip: int = 0, limit: int = 50, order_by: str = None
    ) -> List[T]:
        """
        Retrieve all records with optional pagination and sorting.

        :param skip: Number of records to skip (default 0).
        :param limit: Maximum number of records to return (default 50).
        :param order_by: Optional field name to order results by.
        :return: List of model instances.
        """
        return await self.repository.all(skip=skip, limit=limit, order_by=order_by)

    async def create(self, **kwargs) -> T:
        """
        Create a new record in the database.

        :param kwargs: Data to create the new record.
        :return: Created model instance.
        """
        return await self.repository.create(obj_in=kwargs)

    async def update(self, record_id: int, **kwargs) -> T:
        """
        Update an existing record by its ID.

        :param record_id: ID of the record to update.
        :param kwargs: Fields and values to update.
        :return: Updated model instance.
        """
        record = await self.get_by_id(record_id)
        return await self.repository.update(obj_current=record, obj_in=kwargs)

    async def delete(self, record_id: int) -> dict:
        """
        Delete a record by its ID.

        :param record_id: ID of the record to delete.
        :return: Dictionary with a deletion success message.
        """
        await self.repository.delete(id=record_id)
        return {"message": f"{self.repository.model.__name__} with id {record_id} deleted successfully"}

    async def get_or_create(self, **kwargs) -> T:
        """
        Retrieve a record if it exists; otherwise, create a new one.

        :param kwargs: Filter criteria and creation data.
        :return: Existing or newly created model instance.
        """
        return await self.repository.get_or_create(obj_in=kwargs, **kwargs)

    async def exists(self, **kwargs) -> bool:
        """
        Check if a record exists matching the given criteria.

        :param kwargs: Filtering criteria.
        :return: True if record exists, False otherwise.
        """
        return await self.repository.exists(**kwargs)

    async def count(self, **kwargs) -> int:
        """
        Count the number of records matching filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: Number of matching records.
        """
        return await self.repository.count(**kwargs)

    @classmethod
    def get_service(cls, db: AsyncSession = Depends(get_db)) -> "BaseService":
        """
        Dependency injection helper to instantiate the service with the correct model.

        Extracts the model type from the generic type hint to automatically
        initialize the service with the proper repository.

        :param db: Async SQLAlchemy session provided by FastAPI Depends.
        :return: Initialized instance of the service class.
        :raises TypeError: If the generic type or model cannot be determined.
        """
        if not hasattr(cls, "__orig_bases__") or not cls.__orig_bases__:
            raise TypeError(f"{cls.__name__} must explicitly define a generic type (e.g., BaseService[User])")

        base = cls.__orig_bases__[0]
        if hasattr(base, "__args__") and base.__args__:
            model = base.__args__[0]
        else:
            raise TypeError(f"Could not determine model for {cls.__name__}")

        return cls(db, model)
