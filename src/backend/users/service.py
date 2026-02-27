from backend.db.db_manager import DBManager
from backend.users.models import UsersOrm
from backend.users.schemas import SUserRegister


class UsersService:
    """
    Service layer for User entities and profile management.
    """

    def __init__(self, db: DBManager):
        """
        Initialize the service with a database manager.
        """
        self.db: DBManager = db

    async def register_user(self, user_data: SUserRegister) -> int:
        """
        Register a new user and return their unique ID.

        Returns:
            The ID of the newly created user record.
        """
        user_id = await self.db.users.add_one(user_data)
        await self.db.commit()
        return user_id

    async def get_user_profile(
        self, attr_name, attr_value: int | str
    ) -> UsersOrm:
        """
        Retrieve a user profile by its ID.

        Raises:
            ValueError: If the user is not found.
        """
        return await self.db.users.get_one_by_field(attr_name, attr_value)

    async def delete_account(self, user_id: int) -> None:
        """
        Remove a user and all associated data from the database.

        Note: CASCADE delete should handle tasks automatically.
        """
        user = await self.get_user_profile(user_id)
        await self.db.users.delete(db_obj=user)
        await self.db.commit()
