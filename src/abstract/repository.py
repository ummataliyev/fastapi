from typing import Type
from typing import TypeVar
from typing import Generic

from fastapi import HTTPException

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def get_by_id(self, record_id: int) -> T:
        """
        Get record by id
        """
        try:
            result = await self.db_session.execute(
                select(self.model).filter_by(id=record_id)
            )
            record = result.scalar_one_or_none()
            if record is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{self.model.__name__} not found"
                )

            return record

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all(self) -> list[T]:
        """
        Get all records
        """
        try:
            result = await self.db_session.execute(select(self.model))
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create(self, **kwargs) -> T:
        """
        Create a new record
        """
        try:
            new_record = self.model(**kwargs)
            self.db_session.add(new_record)
            await self.db_session.commit()
            await self.db_session.refresh(new_record)
            return new_record

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, record_id: int, **kwargs) -> T:
        """
        Update an existing record
        """
        try:
            record = await self.get_by_id(record_id)
            for key, value in kwargs.items():
                setattr(record, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(record)
            return record

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(self, record_id: int) -> dict:
        """
        Delete an existing record
        """
        try:
            record = await self.get_by_id(record_id)
            await self.db_session.delete(record)
            await self.db_session.commit()
            return {"message": f"{self.model.__name__} deleted successfully"}

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
