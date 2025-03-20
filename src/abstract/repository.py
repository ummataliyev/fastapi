from typing import Any
from typing import Type
from typing import List
from typing import TypeVar
from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.abstract.interface import IRepository

T = TypeVar("T")


class BaseRepository(IRepository):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def create(self, obj_in: Any, **kwargs: Any) -> T:
        """
        Create a new record
        """
        try:
            record = self.model(
                **obj_in if isinstance(obj_in, dict) else obj_in.__dict__, **kwargs
            )
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
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[T]:
        """
        Get all records with pagination and sorting
        """
        try:
            query = select(self.model).offset(skip).limit(limit)
            if sort_field:
                column = getattr(self.model, sort_field, None)
                if column is not None:
                    order_func = getattr(column, sort_order or "asc")
                    query = query.order_by(order_func())
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise e

    async def f(self, **kwargs: Any) -> List[T]:
        """
        Filter records
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
        Get or create a record
        """
        try:
            record = await self.get(**kwargs)
            if record:
                return record
            return await self.create(obj_in, **kwargs)
        except SQLAlchemyError as e:
            raise e
