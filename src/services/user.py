"""
User service
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.abstract.service import BaseService


class UserService(BaseService[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)
