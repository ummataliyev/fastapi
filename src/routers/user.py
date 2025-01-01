"""
User routes
"""
from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemes.user import User
from src.schemes.user import UserRead
from src.services.user import UserService
from src.response.user import UserResponse
from src.abstract.scheme import APIResponse

from db.storage.postgres import get_db

router = APIRouter()


@router.get("/users/{id}", response_model=APIResponse)
async def get_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    response = UserResponse()

    user_service = UserService(db)
    try:
        user = await user_service.get_by_id(user_id)
    except ValueError as e:
        return response.get_error_response(str(e))

    if user is None:
        return response.user_not_found()

    return response.get_user(user)


@router.get("/users/", response_model=list[UserRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    users = await user_service.get_all()

    return users


@router.post("/users/", response_model=APIResponse)
async def create_user(
    user: User,
    db: AsyncSession = Depends(get_db)
):
    response = UserResponse()
    user_service = UserService(db)
    new_user = await user_service.create(**user.dict())

    return response.create(new_user)


@router.patch("/users/{id}", response_model=APIResponse)
async def update_user(
    user_id: int,
    user: User,
    db: AsyncSession = Depends(get_db)
):
    response = UserResponse()
    user_service = UserService(db)

    try:
        updated_user = await user_service.update(user_id, **user.dict())
    except ValueError:
        return response.user_not_found()

    return response.update(updated_user)


@router.delete("/users/{id}", response_model=APIResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    response = UserResponse()
    user_service = UserService(db)

    try:
        result = await user_service.delete(user_id)
    except ValueError as e:
        return response.get_error_response(message=str(e))

    return response.delete(result["message"])
