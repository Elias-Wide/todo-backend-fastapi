from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repository import SQLAlchemyRepository
from backend.tasks.models import TasksOrm
from backend.tasks.schemas import STask
from backend.users.schemas import SUser


class UsersRepository(SQLAlchemyRepository):
    """
    Repository for managing Task entity database operations.
    """

    model = TasksOrm

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self) -> list[STask]:
        """
        Retrieves all task records from the database.

        Returns:
            List of STask objects representing all tasks in the system.
        """
        model_objs = await super().find_all(self.session)
        return [SUser.model_validate(obj) for obj in model_objs]

    async def get_user_by_name(self, username: str) -> SUser | None:
        """
        Retrieves a user by their username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            An SUser object if found, otherwise None.
        """
        model_obj = await self.get_one_by_field(
            self.session, 'username', username
        )
        return SUser.model_validate(model_obj) if model_obj else None

    async def get_user_by_pk(self, user_id: int) -> SUser:
        self.session = self.session
        return await self.get_one_by_field(self.session, 'id', user_id)

    async def get_user_by_tg_id(self, user_id: int) -> SUser:
        self.session = self.session
        return await self.get_one_by_field(self.session, 'id', user_id)
