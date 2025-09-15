"""
Repository for User model.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.interfaces.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository class for performing async database operations on the User model.

    Inherits:
        - BaseRepository[User]: Provides generic CRUD and query operations
          for the User entity.

    Attributes:
        db_session (AsyncSession): Async SQLAlchemy session used for database access.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the UserRepository with an async database session.

        :param db_session: Async SQLAlchemy session for User model operations.
        """
        super().__init__(db_session, User)
