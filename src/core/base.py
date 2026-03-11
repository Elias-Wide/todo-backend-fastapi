from abc import ABC, abstractmethod
from typing import Any, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from src.db.database import Model


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


class BaseSecurity(ABC):
    """Abstract base class for password hashing and verification."""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Generate a secure hash from a plain-text password."""
        pass

    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify the password against the provided hash."""
        pass


class BaseService(ABC):
    """Abstract base class for service layer."""

    @abstractmethod
    async def create(self, data):
        """Create a new record."""
        pass

    @abstractmethod
    async def get_all(self):
        """Retrieve all records."""
        pass

    @abstractmethod
    async def delete(self, record_id: int):
        """Delete a record by its ID."""
        pass


class BaseApiManager(SingletonMeta):
    """Abstract Base Class for managing FastAPI route registration."""

    @abstractmethod
    def discover_routers(self):
        """Locate and load routers from the filesystem."""
        pass

    @abstractmethod
    def register_routes(self, app: FastAPI):
        """Include loaded routers into the FastAPI application."""
        pass
