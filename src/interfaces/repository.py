"""
Base Repository
"""

from typing import Any
from typing import Type
from typing import List
from typing import TypeVar
from typing import Generic
from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.interface import IRepository


T = TypeVar("T")


class BaseRepository(IRepository[T], Generic[T]):
    """
    Base repository implementation of IRepository interface for async SQLAlchemy operations.

    Provides generic CRUD operations and common query methods for any SQLAlchemy model.
    Designed to be inherited by concrete repositories for specific entity types.
    """

    def __init__(self, db_session: AsyncSession, model: Type[T]):
        """
        Initialize the repository with an async database session and model.

        :param db_session: Async SQLAlchemy session for database access.
        :param model: SQLAlchemy model class representing the entity.
        """
        self.db_session = db_session
        self.model = model

    async def create(self, obj_in: Any, **kwargs: Any) -> T:
        """
        Create a new record in the database.

        :param obj_in: Input data as dict or model instance.
        :param kwargs: Additional keyword arguments to pass to the model constructor.
        :return: The created and persisted model instance.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            data = obj_in if isinstance(obj_in, dict) else obj_in.__dict__
            record = self.model(**data, **kwargs)
            self.db_session.add(record)
            await self.db_session.commit()
            await self.db_session.refresh(record)
            return record
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise e

    async def update(self, obj_current: T, obj_in: Any) -> T:
        """
        Update an existing record in the database.

        :param obj_current: Existing model instance to update.
        :param obj_in: Input data as dict or model instance containing new values.
        :return: The updated model instance.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            update_data = obj_in if isinstance(obj_in, dict) else obj_in.__dict__
            for key, value in update_data.items():
                setattr(obj_current, key, value)
            self.db_session.add(obj_current)
            await self.db_session.commit()
            await self.db_session.refresh(obj_current)
            return obj_current
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise e

    async def get(self, **kwargs: Any) -> Optional[T]:
        """
        Retrieve a single record matching the filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: Model instance if found, else None.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            result = await self.db_session.execute(
                select(self.model).filter_by(**kwargs)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e

    async def delete(self, **kwargs: Any) -> None:
        """
        Delete a single record matching the filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :raises ValueError: If no record is found to delete.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            record = await self.get(**kwargs)
            if record is None:
                raise ValueError("Record not found")
            await self.db_session.delete(record)
            await self.db_session.commit()
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise e

    async def all(
        self,
        skip: int = 0,
        limit: int = 50,
        order_by: Optional[str] = None,
    ) -> List[T]:
        """
        Retrieve all records with pagination and optional sorting.

        :param skip: Number of records to skip.
        :param limit: Maximum number of records to return.
        :param order_by: Optional sorting string, e.g., 'field_name asc' or 'field_name desc'.
        :return: List of model instances.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            query = select(self.model).offset(skip).limit(limit)
            if order_by:
                parts = order_by.strip().split()
                column_name = parts[0]
                direction = parts[1].lower() if len(parts) > 1 else "asc"
                column = getattr(self.model, column_name, None)
                if column is not None:
                    order_func = getattr(column, direction)
                    query = query.order_by(order_func())
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise e

    async def filter(self, **kwargs: Any) -> List[T]:
        """
        Retrieve records matching specific filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: List of matching model instances.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            result = await self.db_session.execute(
                select(self.model).filter_by(**kwargs)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise e

    async def get_or_create(self, obj_in: Any, **kwargs: Any) -> T:
        """
        Retrieve a record if it exists; otherwise, create a new one.

        :param obj_in: Input data to create if record does not exist.
        :param kwargs: Filtering criteria to check existence.
        :return: Existing or newly created model instance.
        """
        record = await self.get(**kwargs)
        if record:
            return record
        return await self.create(obj_in, **kwargs)

    async def exists(self, **kwargs: Any) -> bool:
        """
        Check if a record exists in the database.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: True if a matching record exists, False otherwise.
        """
        record = await self.get(**kwargs)
        return record is not None

    async def count(self, **kwargs: Any) -> int:
        """
        Count the number of records matching specific filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: Number of matching records.
        :raises SQLAlchemyError: If database operation fails.
        """
        query = select(self.model).filter_by(**kwargs)
        result = await self.db_session.execute(query)
        return len(result.scalars().all())
