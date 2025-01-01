from sqlalchemy.ext.asyncio import AsyncSession
from src.abstract.repository import BaseRepository

from typing import Type
from typing import TypeVar
from typing import Generic


T = TypeVar('T')


class BaseService(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.repository = BaseRepository(db_session, model)

    async def get_by_id(self, record_id: int) -> T:
        return await self.repository.get_by_id(record_id)

    async def get_all(self) -> list[T]:
        return await self.repository.get_all()

    async def create(self, **kwargs) -> T:
        return await self.repository.create(**kwargs)

    async def update(self, record_id: int, **kwargs) -> T:
        return await self.repository.update(record_id, **kwargs)

    async def delete(self, record_id: int) -> dict:
        return await self.repository.delete(record_id)
