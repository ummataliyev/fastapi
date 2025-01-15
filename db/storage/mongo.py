"""
Mongo connection
"""
from motor import motor_asyncio

from libs.environs import env

MONGODB_URL = env.str('MONGODB_URL')
MONGO_ENABLED = env.bool("MONGO_ENABLED", default=False)


class MongoDB:
    """
    MongoDB client configuration for establishing a connection
    """
    def __init__(self, uri: str):
        self.__client = motor_asyncio.AsyncIOMotorClient(uri)
        if 'mongodb://' in uri:
            self.__db = self.__client.get_database()
        else:
            self.__db = self.__client.get_database('default_db')

    async def close(self):
        """
        Close the MongoDB connection
        """
        self.__client.close()


if MONGO_ENABLED:
    mongo_client = MongoDB(MONGODB_URL)
