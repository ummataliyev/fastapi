"""
Dynamic databae abstraction
"""

from typing import List
from typing import TypeVar
from typing import Optional
from typing import Generic

from abc import ABC
from abc import abstractmethod


T = TypeVar("T")


class IRepository(Generic[T], ABC):
    """
    Generic repository interface for async data access operations.
    """

    @abstractmethod
    async def create(self, obj_in: T, **kwargs) -> T:
        """
        Create a new entity and return the saved instance.
        """
        ...

    @abstractmethod
    async def update(self, obj_current: T, obj_in: T) -> T:
        """
        Update an existing entity and return the updated instance.
        """
        ...

    @abstractmethod
    async def get(self, **kwargs) -> Optional[T]:
        """
        Retrieve one entity instance based on filter criteria.
        """
        ...

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        """
        Delete one entity instance based on filter criteria.
        """
        ...

    @abstractmethod
    async def all(
        self,
        skip: int = 0,
        limit: int = 50,
        order_by: Optional[str] = None,
    ) -> List[T]:
        """
        Retrieve all entity instances with pagination and optional sorting.
        """
        ...

    @abstractmethod
    async def filter(self, **kwargs) -> List[T]:
        """
        Filter and retrieve a list of entity instances based on criteria.
        """
        ...

    @abstractmethod
    async def get_or_create(self, obj_in: T, **kwargs) -> T:
        """
        Retrieve an entity if it exists, or create it if it doesn't.
        """
        ...

    @abstractmethod
    async def exists(self, **kwargs) -> bool:
        """
        Check if an entity exists based on filter criteria.
        """
        ...

    @abstractmethod
    async def count(self, **kwargs) -> int:
        """
        Count entities based on filter criteria.
        """
        ...
