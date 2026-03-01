from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.database import Model

if TYPE_CHECKING:
    from backend.tasks.models import TasksOrm
from backend.users.constants import TOKEN_HASH_LENGTH


class UsersOrm(Model):
    """
    Represent a system user and their Telegram integration data.

    Attributes:
        username: Unique login name for the user.
        password_hash: Securely stored password hash.
        tg_id: Telegram account ID for bot interaction.
        created_at: Timestamp when the user was registered.
        refresh_tokens: List of active or expired session tokens.
    """

    username: Mapped[str] = mapped_column(String(), unique=True)
    password_hash: Mapped[str] = mapped_column(String())
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    refresh_tokens: Mapped[list['RefreshTokensOrm']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    tasks: Mapped[List['TasksOrm']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        """Technical representation of the user instance."""
        return f'<User(id={self.id}, username={self.username})>'

    def __str__(self) -> str:
        """User-friendly string representation (display name)."""
        return f'User: {self.username}'


class RefreshTokensOrm(Model):
    """
    Represents a refresh token for user authentication.

    Attributes:
        id: Unique identifier for the token.
        user_id: ID of the user associated with this token.
        token_hash: Hashed version of the refresh token.
        expires_at: Expiration timestamp for the token.
        revoked: Indicates if the token has been manually invalidated.
        created_at: Timestamp when the token was issued.
        user: Relationship to the UsersOrm model.
    """

    __tablename__ = 'refresh_tokens'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    token_hash: Mapped[str] = mapped_column(
        String(TOKEN_HASH_LENGTH), unique=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True
    )
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped[UsersOrm] = relationship(back_populates='refresh_tokens')
