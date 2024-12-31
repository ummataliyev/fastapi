from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.abstract.service import BaseService


class UserService(BaseService[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, User)
