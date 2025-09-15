from motor import motor_asyncio

from libs.environs import env

MONGO_IS_ENABLED = env.bool("MONGO_IS_ENABLED", default=False)
MONGODB_URL = env.str('MONGODB_URL', default='mongodb://localhost:27017')


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


if MONGO_IS_ENABLED:
    mongo_client = MongoDB(MONGODB_URL)
