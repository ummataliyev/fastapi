from fastapi import HTTPException

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, user_id: int) -> User:
        try:
            result = await self.db_session.execute(
                select(User).filter_by(id=user_id)
            )
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all(self) -> list[User]:
        try:
            result = await self.db_session.execute(select(User))
            fastapi_items = result.scalars().all()
            return fastapi_items
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create(self, name: str) -> User:
        try:
            new_item = User(name=name)
            self.db_session.add(new_item)
            await self.db_session.commit()
            await self.db_session.refresh(new_item)
            return new_item
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, user_id: int, name: str) -> User:
        try:
            fastapi_item = await self.get_by_id(user_id)
            fastapi_item.name = name
            await self.db_session.commit()
            await self.db_session.refresh(fastapi_item)
            return fastapi_item
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(self, user_id: int) -> dict:
        try:
            fastapi_item = await self.get_by_id(user_id)
            await self.db_session.delete(fastapi_item)
            await self.db_session.commit()
            return {"message": "Item deleted successfully"}
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
