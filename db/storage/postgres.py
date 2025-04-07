"""
Database connection
"""
from urllib.parse import quote

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from libs.environs import env


DB_USER = env.str('DB_USER')
DB_NAME = env.str('DB_NAME')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DB_PASSWORD = quote(env.str('DB_PASSWORD'))


db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" # noqa

Base = declarative_base()

engine = create_async_engine(
    url=db_url,
    echo=True
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session