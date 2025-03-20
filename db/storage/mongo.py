"""
MongoDB connection
"""
from motor.motor_asyncio import AsyncIOMotorClient
from libs.environs import env

MONGODB_URL = env.str("MONGODB_URL", default="")
MONGO_DB_NAME = env.str("MONGO_DB_NAME", "default_db")
MONGO_IS_ENABLED = env.bool("MONGO_IS_ENABLED", default=False)


class MongoDB:
    """
    MongoDB client configuration for establishing a connection
    """
    def __init__(self, uri: str, db_name: str):
        if not uri:
            raise ValueError("MONGODB_URL is empty but MongoDB is enabled!")

        self.__client = AsyncIOMotorClient(uri)
        self.__db = self.__client[db_name]

    async def close(self):
        """
        Close the MongoDB connection
        """
        self.__client.close()

    def get_db(self):
        """
        Returns the database instance
        """
        return self.__db


if MONGO_IS_ENABLED:
    mongo_client = MongoDB(MONGODB_URL, MONGO_DB_NAME)


async def get_mongo_db():
    """
    Dependency function to get the MongoDB database instance
    """
    if not mongo_client:
        raise RuntimeError("MongoDB is disabled but requested!")

    yield mongo_client.get_db()
