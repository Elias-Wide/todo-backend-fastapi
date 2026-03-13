from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import RefreshTokensOrm
from src.repositories.base import SQLAlchemyRepository


class AuthRepository(SQLAlchemyRepository):
    """
    Repository for managing authentication and refresh tokens.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_refresh_token(
        self, user_id: int, token_hash: str, expires_at: datetime
    ) -> RefreshTokensOrm:
        """
        Store a new refresh token hash in the database.

        Returns:
            The created RefreshTokensOrm instance.
        """
        token = RefreshTokensOrm(
            user_id=user_id, token_hash=token_hash, expires_at=expires_at
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_refresh_token(
        self, token_hash: str
    ) -> Optional[RefreshTokensOrm]:
        """
        Retrieve a refresh token by its unique hash.

        Returns:
            The token record if found, otherwise None.
        """
        return await self.session.scalar(
            select(RefreshTokensOrm).where(
                RefreshTokensOrm.token_hash == token_hash
            )
        )

    async def delete_refresh_token(self, token_obj: RefreshTokensOrm) -> None:
        """
        Remove a refresh token record from the database.
        """
        return await super().delete(token_obj)
