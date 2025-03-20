"""
User routers
"""
from fastapi import Depends
from fastapi import APIRouter

from src.schemes.user import User
from src.services.user import UserService
from src.response.user import UserResponse
from src.abstract.scheme import BaseScheme

router = APIRouter()
response = UserResponse()


@router.get("/{id}", response_model=BaseScheme)
async def get_by_id(
    id: int,
    service: UserService = Depends(UserService.get_service)
):
    """
    Get a user by ID
    """
    try:
        user = await service.get_by_id(id)
        return response.get_user(user)
    except ValueError:
        return response.user_not_found()
    except Exception as e:
        return response.get_error_response(f"An error occurred: {str(e)}")


@router.get("/", response_model=BaseScheme)
async def get_all(
    service: UserService = Depends(UserService.get_service)
):
    """
    Get all users
    """
    try:
        users = await service.get_all()
        return response.get_all(users)
    except Exception as e:
        return response.get_error_response(f"An error occurred: {str(e)}")


@router.post("/", response_model=BaseScheme, status_code=201)
async def create_user(
    user: User,
    service: UserService = Depends(UserService.get_service)
):
    """
    Create a new user
    """
    try:
        new_user = await service.create(**user.dict(exclude_unset=True))
        return response.create(new_user)
    except Exception as e:
        return response.get_error_response(f"An error occurred: {str(e)}")


@router.patch("/{id}", response_model=BaseScheme)
async def update_user(
    id: int,
    user: User,
    service: UserService = Depends(UserService.get_service)
):
    """
    Update an existing user
    """
    try:
        updated_user = await service.update(id, **user.dict(exclude_unset=True))
        return response.update(updated_user)
    except ValueError:
        return response.user_not_found()
    except Exception as e:
        return response.get_error_response(f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=BaseScheme)
async def delete_user(
    id: int,
    service: UserService = Depends(UserService.get_service)
):
    """
    Delete a user
    """
    try:
        result = await service.delete(id)
        return response.delete(result["message"])
    except ValueError:
        return response.user_not_found()
    except Exception as e:
        return response.get_error_response(f"An error occurred: {str(e)}")
