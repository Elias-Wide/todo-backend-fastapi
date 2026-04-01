from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pydantic import BaseModel

from db.database import Model


class SingletonMeta:
    """
    Abstract base class for Singleton implementation.

    Ensures that only one instance of the manager exists
    throughout the application.
    """

    _instance: Optional[Any] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonMeta, cls).__new__(cls)
        return cls._instance


class AbstractRepository(ABC):
    """
    Abstract repository class.
    Defining the interface for database operations."""

    @classmethod
    @abstractmethod
    async def add_one(cls, model_data: BaseModel) -> int:
        """Creates a new record in the database."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def find_all(cls) -> List[Model]:
        """Retrieves all records from the database."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def delete(cls, record_id: int):
        """Deletes a record by its ID."""
        raise NotImplementedError
