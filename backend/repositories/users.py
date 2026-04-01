from sqlalchemy.ext.asyncio import AsyncSession

from models.users import UsersOrm
from repositories.base import SQLAlchemyRepository
from schemas.tasks import STask
from schemas.users import SUser, SUserLoginRequest


class UsersRepository(SQLAlchemyRepository):
    """
    Repository for managing Task entity database operations.
    """

    model = UsersOrm

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, username: str, password_hash: str) -> SUser:
        """
        Creates a new user record in the database.

        Args:
            username: The username of the new user.
            password_hash: The hashed password of the new user.
        """
        user = self.model(username=username, password_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()
        return user

    async def find_all(self) -> list[STask]:
        """
        Retrieves all task records from the database.

        Returns:
            List of STask objects representing all tasks in the system.
        """
        model_objs = await super().find_all(self.session)
        return [SUser.model_validate(obj) for obj in model_objs]

    async def get_user_by_id(self, user_id: int) -> SUserLoginRequest | None:
        """
        Retrieves a user by their unique ID.

        Args:
            user_id: The integer ID of the user to retrieve.

        Returns:
            An SUserLoginRequest object if found, otherwise None.
        """
        model_obj = await self.get_one_by_field(
            attr_name='id', attr_value=user_id
        )
        return (
            SUserLoginRequest.model_validate(model_obj) if model_obj else None
        )

    async def get_user_by_username(
        self, username: str
    ) -> SUserLoginRequest | None:
        """
        Retrieves a user by their username.

        Args:
            username: The string username of the user to retrieve.

        Returns:
            An SUserLoginRequest object if found, otherwise None.
        """
        model_obj = await self.get_one_by_field(
            attr_name='username', attr_value=username
        )
        return (
            SUserLoginRequest.model_validate(model_obj) if model_obj else None
        )
