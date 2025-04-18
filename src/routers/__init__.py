"""
Initialize routers
"""
from fastapi import Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from src.routers import user

routers = APIRouter()
home_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@routers.get("/", response_description="Homepage", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "github_username": "ummataliyev"}
    )


routers.include_router(user.router, prefix="/users", tags=["Users"])
