from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.abstract.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, User)