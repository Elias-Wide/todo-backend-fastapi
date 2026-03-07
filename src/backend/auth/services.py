from datetime import datetime, timedelta, timezone

from backend.auth.schemas import STokenPair
from backend.auth.security import security
from backend.auth.tokens import tokens
from backend.core.config import settings
from backend.core.exceptions import (
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserNotFoundError,
)
from backend.db.db_manager import DBManager
from backend.users.models import UsersOrm


class AuthServiceJWT:
    def __init__(self, db: DBManager):
        self.db = db

    async def _get_user_or_raise(self, username: str, password: str):
        user: UsersOrm = await self.db.users.get_user_by_username(username)
        if not user or not security.verify_password(
            password, user.password_hash
        ):
            raise InvalidCredentialsError
        return user

    async def login(self, name: str, password: str):
        user = await self._get_user_or_raise(name, password)
        pair = await self._issue_tokens(user.id)
        return pair.access_token, pair.refresh_token

    async def refresh(self, raw_refresh_token: str):
        stored = await self._get_valid_refresh(raw_refresh_token)
        user: UsersOrm = await self._get_user_for_token(stored.user_id)
        await self.db.auth.delete_refresh_token(stored)
        return await self._issue_tokens(user.id)

    async def delete_refresh_token(self, raw_refresh_token: str):
        stored = await self._get_valid_refresh(raw_refresh_token)
        if not stored or stored.revoked:
            raise RefreshTokenNotFoundError
        await self.db.auth.delete_refresh_token(stored)

    async def _get_valid_refresh(self, raw_refresh_token: str):
        token_hash = tokens.hash_token(raw_refresh_token)
        stored = await self.db.auth.get_refresh_token(token_hash)
        if not stored or stored.revoked:
            raise RefreshTokenNotFoundError
        now = datetime.now(timezone.utc)
        if stored.expires_at <= now:
            await self.db.auth.delete_refresh_token(stored)
            raise RefreshTokenExpiredError
        return stored

    async def _get_user_for_token(self, user_id: int):
        user = await self.db.users.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return user

    def _refresh_expiry(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(
            minutes=settings.auth.refresh_token_expires_minutes
        )

    async def _issue_tokens(self, user_id: int) -> STokenPair:
        access_token = tokens.create_access_token(user_id)
        refresh_token = tokens.create_refresh_token()
        refresh_hash = tokens.hash_token(refresh_token)
        expires_at = self._refresh_expiry()
        await self.db.auth.create_refresh_token(
            user_id=user_id, token_hash=refresh_hash, expires_at=expires_at
        )
        await self.db.session.commit()
        return STokenPair(
            access_token=access_token, refresh_token=refresh_token
        )
