from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from backend.db.database import Model


class AbstractRepository(ABC):
    """
    Abstract repository class.
    Defining the interface for database operations."""

    @abstractmethod
    @classmethod
    async def add_one(cls, model_data: BaseModel) -> int:
        """Creates a new record in the database."""
        raise NotImplementedError

    @abstractmethod
    @classmethod
    async def find_all(cls) -> List[Model]:
        """Retrieves all records from the database."""
        raise NotImplementedError

    @abstractmethod
    @classmethod
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
