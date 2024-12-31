from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserRead
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
