from backend.core.exceptions import UserAlreadyExistsError
from backend.models.users import UsersOrm
from backend.schemas.users import SUserRegister
from backend.services.auth.security import security
from backend.services.base import BaseService


class UsersService(BaseService):
    """
    Service layer for User entities and profile management.
    """

    async def register_user(self, user_data: SUserRegister) -> int:
        """
        Register a new user and return their unique ID.

        Returns:
            The ID of the newly created user record.
        """
        existing = await self.db.users.get_user_by_username(user_data.username)
        if existing:
            raise UserAlreadyExistsError
        user = await self.db.users.create_user(
            username=user_data.username,
            password_hash=security.hash_password(user_data.password),
        )
        await self.db.session.commit()
        return user

    async def get_user_profile(self, attr_value: int | str) -> UsersOrm:
        """
        Retrieve a user profile by its ID or username.

        Raises:
            ValueError: If the user is not found.
        """
        if str(attr_value).isdigit():
            return await self.db.users.get_user_by_id(attr_value)
        return await self.db.users.get_user_by_username(attr_value)

    async def delete_account(self, user_id: int) -> None:
        """
        Remove a user and all associated data from the database.

        Note: CASCADE delete should handle tasks automatically.
        """
        user = await self.get_user_profile(user_id)
        await self.db.users.delete(db_obj=user)
        await self.db.commit()
