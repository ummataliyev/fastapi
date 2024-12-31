from fastapi import FastAPI
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import PlainTextResponse

from db.storage.postgres import async_session
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.routers import routers, home_router


app = FastAPI(
    title="AsiaLine API",
    description="AsiaLine API documentation",
    version="1.0.42",
)

app.include_router(routers)
app.include_router(home_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with async_session() as session:
        request.state.db = session
        response = await call_next(request)
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc), status_code=400)


# Event to run tasks at app startup
@app.on_event('startup')
async def on_startup():
    scheduler = AsyncIOScheduler()
    scheduler.start()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
