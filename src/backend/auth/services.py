from backend.auth.security import Security, security
from backend.core.exceptions import InvalidCredentialsError
from backend.users.service import UsersService


class AuthServiceJWT:
    def __init__(self, users: UsersService, security: Security):
        self.user_service = users
        self.security = security

    async def _get_user_or_raise(self, username: str, password: str):
        user = await self.user_service.get_user_profile('username', username)
        if not user or not security.verify_password(
            password, user.hashed_password
        ):
            raise InvalidCredentialsError
        return user

    # async def authenticate_user(self, username: str, password: str):
