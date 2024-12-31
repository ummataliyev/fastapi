from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.repository = UserRepository(db_session)

    async def get_by_id(self, user_id: int):
        return await self.repository.get_by_id(user_id)

    async def get_all(self):
        return await self.repository.get_all()

    async def create(self, name: str):
        return await self.repository.create(name)

    async def update(self, user_id: int, name: str):
        return await self.repository.update(user_id, name)

    async def delete(self, user_id: int):
        return await self.repository.delete(user_id)
