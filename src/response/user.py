from src.models.user import User
from src.schemas.user import UserRead
from src.abstract.response import BaseResponse


class UserResponse(BaseResponse[User]):
    def __init__(self):
        super().__init__(model=User)

    def get_user(self, user: User) -> dict:
        """
        Return the user-specific response for GET
        """
        return self.get_success_response(user)

    def user_not_found(self) -> dict:
        """
        Return a not found response for user
        """
        return self.get_error_response("User not found")

    def create(self, user: User) -> dict:
        """
        Return a success response for user creation (POST)
        """
        user_data = UserRead.from_orm(user)
        return {
            "status": "success",
            "message": "User created successfully",
            "data": user_data
        }

    def update(self, user: User) -> dict:
        """
        Return a success response for user update (PATCH)
        """
        return self.get_update_success_response(user)

    def delete(self, message: str) -> dict:
        """
        Return a success response for user deletion (DELETE)
        """
        return {
            "status": "success",
            "message": message,
            "data": None
        }
