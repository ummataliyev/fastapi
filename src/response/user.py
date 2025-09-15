"""
User response
"""

from typing import List

from src.models.user import User
from src.schemas.user import UserRead
from src.interfaces.response import BaseResponse
from src.interfaces.scheme import BaseScheme


class UserResponse(BaseResponse[User]):
    """
    Response handler for User-related API endpoints
    """

    def __init__(self):
        super().__init__(model=User)

    def _to_schema(self, user: User) -> UserRead:
        """
        Convert User model to UserRead schema
        """
        return UserRead.from_orm(user)

    def get_user(self, user: User) -> BaseScheme:
        return self.success(record=self._to_schema(user))

    def user_not_found(self) -> BaseScheme:
        return self.error("User not found")

    def create(self, user: User) -> BaseScheme:
        return self.success(record=self._to_schema(user), action="create")

    def update(self, user: User) -> BaseScheme:
        return self.success(record=self._to_schema(user), action="update")

    def delete(self) -> BaseScheme:
        return self.success(record=None, action="delete")

    def get_all(self, users: List[User]) -> BaseScheme:
        return self.success(record=[self._to_schema(u) for u in users])
