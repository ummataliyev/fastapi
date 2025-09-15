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
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def create(self, obj_in: Any, **kwargs: Any) -> T:
        """
        Create a new record
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
        Update an existing record
        """
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.__dict__

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
        Get one record by filter
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
        Delete one record by filter
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
        Get all records with pagination and optional sorting
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
        Filter records by criteria
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
        Get a record if exists, otherwise create it
        """
        record = await self.get(**kwargs)
        if record:
            return record
        return await self.create(obj_in, **kwargs)

    async def exists(self, **kwargs: Any) -> bool:
        """
        Check if a record exists
        """
        record = await self.get(**kwargs)
        return record is not None

    async def count(self, **kwargs: Any) -> int:
        """
        Count records matching filter criteria
        """
        query = select(self.model).filter_by(**kwargs)
        result = await self.db_session.execute(query)
        return len(result.scalars().all())
