"""
User Response
"""

from typing import List

from src.models.user import User
from src.schemas.user import UserRead
from src.interfaces.response import BaseResponse
from src.interfaces.scheme import BaseScheme


class UserResponse(BaseResponse[User]):
    """
    Handles API responses for User entities.

    Inherits:
        - BaseResponse[User]: Provides generic success and error response
          methods for model instances.

    Methods:
        - get_user: Return a single user in success response.
        - user_not_found: Return an error response if user is not found.
        - create: Return a success response after creating a user.
        - update: Return a success response after updating a user.
        - delete: Return a success response after deleting a user.
        - get_all: Return a success response with a list of users.
    """

    def __init__(self):
        """
        Initialize the response handler with the User model.
        """
        super().__init__(model=User)

    def _to_schema(self, user: User) -> UserRead:
        """
        Convert a User model instance to a UserRead Pydantic schema.

        :param user: User model instance to convert.
        :return: UserRead schema instance.
        """
        return UserRead.from_orm(user)

    def get_user(self, user: User) -> BaseScheme:
        """
        Generate a success response containing a single user.

        :param user: User model instance.
        :return: BaseScheme with user data.
        """
        return self.success(record=self._to_schema(user))

    def user_not_found(self) -> BaseScheme:
        """
        Generate an error response indicating that the user was not found.

        :return: BaseScheme with error message.
        """
        return self.error("User not found")

    def create(self, user: User) -> BaseScheme:
        """
        Generate a success response after creating a user.

        :param user: User model instance that was created.
        :return: BaseScheme with user data and create action.
        """
        return self.success(record=self._to_schema(user), action="create")

    def update(self, user: User) -> BaseScheme:
        """
        Generate a success response after updating a user.

        :param user: User model instance that was updated.
        :return: BaseScheme with user data and update action.
        """
        return self.success(record=self._to_schema(user), action="update")

    def delete(self) -> BaseScheme:
        """
        Generate a success response after deleting a user.

        :return: BaseScheme indicating delete action.
        """
        return self.success(record=None, action="delete")

    def get_all(self, users: List[User]) -> BaseScheme:
        """
        Generate a success response containing a list of users.

        :param users: List of User model instances.
        :return: BaseScheme with list of user data.
        """
        return self.success(record=[self._to_schema(u) for u in users])
