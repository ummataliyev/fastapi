"""
User Service
"""

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.interfaces.service import BaseService


class UserService(BaseService[User]):
    """
    Service class for User entity.

    Inherits:
        - BaseService[User]: Provides generic async CRUD and query operations
          for User model.

    Attributes:
        repository: Inherited BaseRepository[User] for database access.
    """

    def __init__(
        self,
        db: AsyncSession,
        model: Type[User] = User
    ):
        """
        Initialize the UserService with async database session.

        :param db: Async SQLAlchemy session.
        :param model: User model class (default: User).
        """
        super().__init__(db, model)
