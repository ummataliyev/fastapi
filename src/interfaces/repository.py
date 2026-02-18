"""
Base Repository
"""

from typing import Any
from typing import Type
from typing import List
from typing import TypeVar
from typing import Generic
from typing import Optional

from sqlalchemy import func
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

    @staticmethod
    def _normalize_input(obj_in: Any) -> dict:
        """
        Convert supported payload types to a plain dictionary.
        """
        if obj_in is None:
            return {}
        if isinstance(obj_in, dict):
            return dict(obj_in)
        if hasattr(obj_in, "model_dump") and callable(obj_in.model_dump):
            return obj_in.model_dump(exclude_unset=True)
        if hasattr(obj_in, "dict") and callable(obj_in.dict):
            return obj_in.dict(exclude_unset=True)
        return {
            key: value
            for key, value in vars(obj_in).items()
            if not key.startswith("_")
        }

    def _uses_soft_delete(self) -> bool:
        """
        Check whether the model supports soft deletion.
        """
        return hasattr(self.model, "deleted_at")

    def _default_filters(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Apply default filtering rules (exclude soft-deleted records).
        """
        filters = dict(kwargs)
        if self._uses_soft_delete() and "deleted_at" not in filters:
            filters["deleted_at"] = None
        return filters

    async def create(self, obj_in: Any, **kwargs: Any) -> T:
        """
        Create a new record in the database.

        :param obj_in: Input data as dict or model instance.
        :param kwargs: Additional keyword arguments to pass to the model constructor.
        :return: The created and persisted model instance.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            data = self._normalize_input(obj_in)
            data.update(kwargs)
            record = self.model(**data)
            self.db_session.add(record)
            await self.db_session.commit()
            await self.db_session.refresh(record)
            return record
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise

    async def update(self, obj_current: T, obj_in: Any) -> T:
        """
        Update an existing record in the database.

        :param obj_current: Existing model instance to update.
        :param obj_in: Input data as dict or model instance containing new values.
        :return: The updated model instance.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            update_data = self._normalize_input(obj_in)
            for key, value in update_data.items():
                setattr(obj_current, key, value)
            self.db_session.add(obj_current)
            await self.db_session.commit()
            await self.db_session.refresh(obj_current)
            return obj_current
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise

    async def get(self, **kwargs: Any) -> Optional[T]:
        """
        Retrieve a single record matching the filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: Model instance if found, else None.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            filters = self._default_filters(kwargs)
            result = await self.db_session.execute(
                select(self.model).filter_by(**filters)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            raise

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
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise

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
            query = select(self.model)
            if self._uses_soft_delete():
                query = query.where(self.model.deleted_at.is_(None))
            if order_by:
                parts = order_by.strip().split()
                column_name = parts[0]
                direction = parts[1].lower() if len(parts) > 1 else "asc"
                if direction not in {"asc", "desc"}:
                    raise ValueError("order_by direction must be 'asc' or 'desc'")
                column = getattr(self.model, column_name, None)
                if column is None:
                    raise ValueError(f"Unknown order_by field: {column_name}")
                query = query.order_by(
                    column.asc() if direction == "asc" else column.desc()
                )
            query = query.offset(skip).limit(limit)
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError:
            raise

    async def filter(self, **kwargs: Any) -> List[T]:
        """
        Retrieve records matching specific filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: List of matching model instances.
        :raises SQLAlchemyError: If database operation fails.
        """
        try:
            filters = self._default_filters(kwargs)
            result = await self.db_session.execute(
                select(self.model).filter_by(**filters)
            )
            return result.scalars().all()
        except SQLAlchemyError:
            raise

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
        payload = self._normalize_input(obj_in)
        payload.update(kwargs)
        return await self.create(payload)

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
        filters = self._default_filters(kwargs)
        query = select(func.count()).select_from(self.model).filter_by(**filters)
        result = await self.db_session.execute(query)
        return result.scalar_one()
