"""
User response
"""
from src.models.user import User
from src.schemes.user import UserRead
from src.abstract.response import BaseResponse
from src.abstract.scheme import BaseScheme


class UserResponse(BaseResponse[User]):
    """
    Response handler for User-related API endpoints
    """

    def __init__(self):
        super().__init__(model=User)

    def get_user(self, user: User) -> BaseScheme:
        """
        Return a success response for retrieving a user
        """
        user_data = UserRead.from_orm(user)
        return self.get_success_response(user_data)

    def user_not_found(self) -> BaseScheme:
        """
        Return an error response when a user is not found
        """
        return self.get_error_response("User not found")

    def create(self, user: User) -> BaseScheme:
        """
        Return a success response for user creation
        """
        user_data = UserRead.from_orm(user)
        return self.get_create_success_response(user_data)

    def update(self, user: User) -> BaseScheme:
        """
        Return a success response for user update
        """
        user_data = UserRead.from_orm(user)
        return self.get_update_success_response(user_data)

    def delete(self, message: str) -> BaseScheme:
        """
        Return a success response for user deletion
        """
        return self.get_delete_success_response()

    def get_all(self, users: list[User]) -> BaseScheme:
        """
        Return a success response for retrieving all users
        """
        user_data = [UserRead.from_orm(user) for user in users]
        return self.get_all_response(user_data)
