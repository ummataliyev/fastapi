"""
Base service class for interacting with repositories
"""
from fastapi import Depends

from typing import List
from typing import Type
from typing import TypeVar
from typing import Generic

from sqlalchemy.ext.asyncio import AsyncSession
from src.abstract.repository import BaseRepository

from db.storage.postgres import get_db

T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        """
        Initialize the BaseService with a database session and model
        """
        self.repository = BaseRepository(db_session, model)

    async def get_by_id(self, record_id: int) -> T:
        """
        Get a record by its ID
        """
        record = await self.repository.get(id=record_id)
        if record is None:
            raise ValueError(f"{self.repository.model.__name__} with id {record_id} not found")
        return record

    async def get_all(self) -> List[T]:
        """
        Get all records with default pagination
        """
        return await self.repository.all()

    async def create(self, **kwargs) -> T:
        """
        Create a new record
        """
        return await self.repository.create(obj_in=kwargs)

    async def update(self, record_id: int, **kwargs) -> T:
        """
        Update an existing record by its ID
        """
        record = await self.get_by_id(record_id)
        return await self.repository.update(obj_current=record, obj_in=kwargs)

    async def delete(self, record_id: int) -> dict:
        """
        Delete a record by its ID
        """
        await self.repository.delete(id=record_id)
        return {"message": f"{self.repository.model.__name__} with id {record_id} deleted successfully"}

    @classmethod
    def get_service(cls, db: AsyncSession = Depends(get_db)) -> "BaseService":
        """
        Creates a service instance for dependency
        """
        if not hasattr(cls, "__orig_bases__") or not cls.__orig_bases__:
            raise TypeError(f"{cls.__name__} must explicitly define a generic type (e.g., BaseService[User])")

        base = cls.__orig_bases__[0]

        if hasattr(base, "__args__") and base.__args__:
            model = base.__args__[0]
        else:
            raise TypeError(f"Could not determine model for {cls.__name__}")

        return cls(db)  # ✅ Pass only db (not model)
