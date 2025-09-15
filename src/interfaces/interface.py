"""
Dynamic databae abstraction
"""

from typing import List
from typing import TypeVar
from typing import Generic
from typing import Optional

from abc import ABC
from abc import abstractmethod


T = TypeVar("T")


class IRepository(Generic[T], ABC):
    """
    Generic repository interface for async data access operations.

    This interface defines standard CRUD operations and common
    query methods for any entity type `T`. It is intended to be
    implemented by concrete repository classes that interact
    with a database or other storage systems.
    """

    @abstractmethod
    async def create(self, obj_in: T, **kwargs) -> T:
        """
        Create a new entity in the data store.

        :param obj_in: The entity instance or data to be created.
        :param kwargs: Optional additional arguments for creation.
        :return: The saved entity instance.
        """
        ...

    @abstractmethod
    async def update(self, obj_current: T, obj_in: T) -> T:
        """
        Update an existing entity in the data store.

        :param obj_current: The current entity instance to update.
        :param obj_in: The new data or entity to update with.
        :return: The updated entity instance.
        """
        ...

    @abstractmethod
    async def get(self, **kwargs) -> Optional[T]:
        """
        Retrieve a single entity instance based on filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: The entity instance if found, otherwise None.
        """
        ...

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        """
        Delete a single entity instance based on filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: None
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
        Retrieve all entity instances with optional pagination and sorting.

        :param skip: Number of records to skip (default 0).
        :param limit: Maximum number of records to return (default 50).
        :param order_by: Optional field name to order results by.
        :return: List of entity instances.
        """
        ...

    @abstractmethod
    async def filter(self, **kwargs) -> List[T]:
        """
        Filter and retrieve a list of entity instances based on criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: List of entity instances matching the criteria.
        """
        ...

    @abstractmethod
    async def get_or_create(self, obj_in: T, **kwargs) -> T:
        """
        Retrieve an entity if it exists, or create it if it doesn't.

        :param obj_in: The entity instance or data to create if not exists.
        :param kwargs: Filtering criteria to check existence.
        :return: Existing or newly created entity instance.
        """
        ...

    @abstractmethod
    async def exists(self, **kwargs) -> bool:
        """
        Check if an entity exists based on filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: True if entity exists, False otherwise.
        """
        ...

    @abstractmethod
    async def count(self, **kwargs) -> int:
        """
        Count the number of entities matching filter criteria.

        :param kwargs: Filtering criteria as key-value pairs.
        :return: Number of matching entities.
        """
        ...
