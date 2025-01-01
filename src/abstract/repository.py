from typing import Type
from typing import TypeVar

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar('T')


class BaseRepository:
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def get_by_id(self, record_id: int) -> T:
        """
        Get record by ID
        """
        result = await self.db_session.execute(
            select(self.model).filter(self.model.id == record_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[T]:
        """
        Get all records
        """
        result = await self.db_session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, **kwargs) -> T:
        """
        Create a new record
        """
        record = self.model(**kwargs)
        self.db_session.add(record)
        await self.db_session.commit()
        await self.db_session.refresh(record)
        return record

    async def update(self, record_id: int, **kwargs) -> T:
        """
        Update an existing record
        """
        result = await self.db_session.execute(
            select(self.model).filter(self.model.id == record_id)
        )
        record = result.scalar_one_or_none()
        if record is None:
            raise ValueError("Record not found")

        for key, value in kwargs.items():
            setattr(record, key, value)

        self.db_session.add(record)
        await self.db_session.commit()
        await self.db_session.refresh(record)

        return record

    async def delete(self, record_id: int) -> dict:
        """
        Delete an existing record
        """
        result = await self.db_session.execute(
            select(self.model).filter(self.model.id == record_id)
        )
        record = result.scalar_one_or_none()
        if record is None:
            raise ValueError("Record not found")

        await self.db_session.delete(record)
        await self.db_session.commit()

        return {"message": f"{self.model.__name__} deleted successfully"}
