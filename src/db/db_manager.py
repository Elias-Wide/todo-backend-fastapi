from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import AuthRepository
from src.db.database import SessionLocal
from src.tasks.repository import TasksRepository
from src.users.repository import UsersRepository


class DBManager:
    """
    Manager for handling database sessions and repository access.
    Implements the Unit of Work pattern.
    """

    def __init__(
        self, session_factory: Callable[[], AsyncSession] = SessionLocal
    ):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.users: UsersRepository | None = None
        self.tasks: TasksRepository | None = None
        self.auth: AuthRepository | None = None
        self._committed = False

    async def __aenter__(self) -> 'DBManager':
        self.session = self.session_factory()
        self.users = UsersRepository(self.session)
        self.tasks = TasksRepository(self.session)
        self.auth = AuthRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Gracefully close the session.
        Rolls back only if an exception occurred.
        """
        try:
            if exc_type or not self._committed:
                await self.session.rollback()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        """
        Explicitly save changes.
        This should be called at the end of successful logic.
        """
        if self.session:
            await self.session.commit()
            self._committed = True
