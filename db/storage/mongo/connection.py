"""
Mongo DB configurations
"""

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from libs.environs import env

MONGO_IS_ENABLED = env.bool("MONGO_IS_ENABLED", default=False)
MONGODB_URL = env.str('MONGODB_URL', default='mongodb://localhost:27017')


class MongoDB:
    """
    MongoDB client configuration.
    """

    def __init__(self, uri: str, db_name: str = "default_db") -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
        self.db: AsyncIOMotorDatabase = (
            self.client.get_default_database()
            if uri.startswith("mongodb://") and "/" in uri
            else self.client[db_name]
        )

    async def close(self) -> None:
        """
        Close the MongoDB connection.
        """
        self.client.close()


mongo_client: MongoDB | None
if MONGO_IS_ENABLED:
    mongo_client = MongoDB(MONGODB_URL)
else:
    mongo_client = None
