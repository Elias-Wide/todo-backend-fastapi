from abc import ABC, abstractmethod

from src.db.db_manager import DBManager


class BaseService:
    """Service layer for business logic."""

    def __init__(self, db: DBManager):
        """Initialize the service with a task repository."""
        self.db: DBManager = db


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
