"""
User service
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemes.user import UserRead
from src.abstract.service import BaseService


class UserService(BaseService[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, User)

    async def get_by_id(self, record_id: int) -> UserRead:
        user = await super().get_by_id(record_id)
        return UserRead.from_orm(user) if user else None

    async def get_all(self) -> list[UserRead]:
        users = await super().get_all()
        return [UserRead.from_orm(user) for user in users]

    async def create(self, **kwargs) -> UserRead:
        user = await super().create(**kwargs)
        return UserRead.from_orm(user)

    async def update(self, record_id: int, **kwargs) -> UserRead:
        user = await super().update(record_id, **kwargs)
        return UserRead.from_orm(user)

    async def delete(self, record_id: int) -> dict:
        return await super().delete(record_id)
