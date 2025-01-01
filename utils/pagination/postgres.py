from typing import Any
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from utils.helpers.pagination import get_count
from utils.helpers.pagination import decode_id
from utils.helpers.pagination import encode_id


class DBPaginator:
    def __init__(
        self,
        db: AsyncSession,
        query: Any,
        model,
        limit: int,
        cursor: Optional[str] = None
    ):
        self.db = db
        self.query = query
        self.limit = limit
        self.model = model
        self.cursor = cursor
        self.next_cursor: Optional[str] = None
        self.previous_cursor: Optional[str] = None

    async def _set_previous_cursor(self, result, is_reversed: bool = False):
        if len(result) > 0:
            query = await self.db.execute(
                self.query.order_by(self.model.id.desc())
            )
            first_id = query.scalar()
            first = result[0].id
            if is_reversed:
                first = result[-1].id
            if first_id and first_id.id != first:
                self.previous_cursor = await encode_id(first)
            else:
                self.previous_cursor = None
        else:
            self.previous_cursor = None

    async def _set_next_cursor(self, result, is_reversed: bool = False):
        if len(result) == self.limit:
            query = await self.db.execute(
                self.query.order_by(self.model.id.asc())
            )
            last_id = query.scalar()
            last = result[-1].id
            if is_reversed:
                last = result[0].id
            if last_id and last_id.id != last:
                self.next_cursor = await encode_id(last)
            else:
                self.next_cursor = None
        else:
            self.next_cursor = None

    async def get_previous(self):
        cursor = await decode_id(self.cursor)
        counter = await get_count(self.db, self.query, self.model)
        if counter < self.limit:
            return await self.get_first()
        query = (
            self.query.filter(self.model.id > cursor)
            .order_by(self.model.id.asc())
            .limit(self.limit)
        )
        temp_results = await self.db.execute(query)
        results = temp_results.unique().scalars().all()
        await self._set_previous_cursor(results, True)
        await self._set_next_cursor(results, True)

        return results, self.previous_cursor, self.next_cursor

    async def get_next(self):
        cursor = await decode_id(self.cursor)
        query = (
            self.query.filter(self.model.id < cursor)
            .order_by(self.model.id.desc())
            .limit(self.limit)
        )
        temp_results = await self.db.execute(query)
        results = temp_results.unique().scalars().all()
        await self._set_previous_cursor(results)
        await self._set_next_cursor(results)

        return results, self.previous_cursor, self.next_cursor

    async def get_first(self):
        query = self.query.order_by(self.model.id.desc()).limit(self.limit)
        temp_results = await self.db.execute(query)
        results = temp_results.unique().scalars().all()
        self.previous_cursor = None
        await self._set_next_cursor(results)

        return results, self.previous_cursor, self.next_cursor
