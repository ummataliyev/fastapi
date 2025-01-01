"""
Initialize routers
"""
from fastapi import Response
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.routers import user


home_router = APIRouter()


@home_router.get(
    path="/",
    include_in_schema=False,
    response_description="Homepage"
)
async def home() -> Response:
    """
    Default home page
    """
    return PlainTextResponse("Welcome to FastAPI!")


routers = APIRouter()

routers.include_router(user.router)
