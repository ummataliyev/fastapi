"""
Database connection
"""
import re
from urllib.parse import quote

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from libs.environs import env

DB_USER = env.str('DB_USER')
DB_NAME = env.str('DB_NAME')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DB_PASSWORD = quote(env.str('DB_PASSWORD'))

db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa

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


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
        Converts `CamelCase` class name
        to `snake_case` table name, adding 's'.

        :return: Pluralized snake_case table name.
        """
        name = re.sub(
            r"(?<!^)(?=[A-Z])",
            "_",
            cls.__name__,
        ).lower()
        pluralized_name = name + "s"
        return pluralized_name


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
