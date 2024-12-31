from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserRead
from src.schemas.user import User

from src.services.user import UserService

from db.storage.postgres import get_db

router = APIRouter()


@router.get("/users/{id}", response_model=UserRead)
async def get_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    return user


@router.get("/users/", response_model=list[UserRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    users = await user_service.get_all()

    return users


@router.post("/users/", response_model=UserRead)
async def create_user(
    user: User,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    new_user = await user_service.create(**user.dict())
    return new_user


@router.patch("/users/{id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user: User,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    updated_user = await user_service.update(user_id, user.name)
    return updated_user


@router.delete("/users/{id}", response_model=dict)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    deleted_message = await user_service.delete(user_id)
    return deleted_message
