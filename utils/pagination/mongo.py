import bson

from typing import Any
from typing import List
from typing import Dict
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection


class MongoPaginator:
    def __init__(
        self,
        collection: AsyncIOMotorCollection,
        query: Dict[str, Any],
        limit: int,
        cursor: Optional[str] = None
    ):
        self.collection = collection
        self.query = query
        self.limit = limit
        self.cursor = bson.ObjectId(cursor) if cursor else None
        self.next_cursor: Optional[str] = None
        self.previous_cursor: Optional[str] = None
        self.sort = -1

    async def has_next(self, last_item: bson.ObjectId) -> bool:
        result = await self.collection.find_one({"_id": {"$lt": last_item}})
        return True if result else False

    async def has_previous(self, first_item: bson.ObjectId) -> bool:
        result = await self.collection.find_one({"_id": {"$gt": first_item}})
        return True if result else False

    async def get_page(self, forward: bool = True) -> List[Dict[str, Any]]:
        if self.cursor:
            if forward:
                self.query['_id'] = {'$lt': self.cursor}
            else:
                self.query['_id'] = {'$gt': self.cursor}

        cursor = (
            self.collection
            .find(self.query)
            .sort('_id', self.sort)
            .limit(self.limit)
        )

        results = await cursor.to_list(length=None)

        if results:
            if await self.has_previous(results[0]['_id']):
                self.previous_cursor = str(results[0]['_id'])
            else:
                self.previous_cursor = None

            if len(results) < self.limit:
                self.next_cursor = None
            else:
                if await self.has_next(results[-1]['_id']):
                    self.next_cursor = str(results[-1]['_id'])
                else:
                    self.next_cursor = None
        else:
            self.next_cursor = None
            self.previous_cursor = None

        return results
