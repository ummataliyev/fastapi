"""
Dynamic databae abstraction
"""
from typing import Any
from typing import List
from typing import Optional


from abc import ABCMeta
from abc import abstractmethod


class IRepository(metaclass=ABCMeta):
    """
    Class representing the repository interface for data access operations
    """

    @abstractmethod
    async def create(self, obj_in: Any, **kwargs: Any) -> Any:
        """
        Create a new entity and return the saved instance
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_current: Any, obj_in: Any) -> Any:
        """
        Update an existing entity and return the saved instance
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs: Any) -> Optional[Any]:
        """
        Retrieve one entity instance based on filter criteria
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs: Any) -> None:
        """
        Delete one entity instance based on filter criteria
        """
        raise NotImplementedError

    @abstractmethod
    async def all(
        self,
        skip: int = 0,
        limit: int = 50,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Any]:
        """
        Retrieve all entity instances with pagination and sorting options
        """
        raise NotImplementedError

    @abstractmethod
    async def f(self, **kwargs: Any) -> List[Any]:
        """
        Filter and retrieve a list of entity instances based on criteria
        """
        raise NotImplementedError

    @abstractmethod
    async def get_or_create(self, obj_in: Any, **kwargs: Any) -> Any:
        """
        Retrieve an entity if it exists, or create it if it doesn't
        """
        raise NotImplementedError
