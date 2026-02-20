from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.database import Model
from backend.users.constants import USERNAME_LENGTH


class Users(Model):
    """
    Represent a system user and their Telegram integration data.

    Stores authentication details, unique identifiers, and metadata
    required for user management and bot interactions.
    """

    username: Mapped[str] = mapped_column(String(USERNAME_LENGTH), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=True)
    tg_username: Mapped[str] = mapped_column(
        String(USERNAME_LENGTH), nullable=True
    )

    def __repr__(self) -> str:
        """Technical representation of the user instance."""
        return f'<User(id={self.id}, username={self.username})>'

    def __str__(self) -> str:
        """User-friendly string representation (display name)."""
        return f'User: {self.username} (TG: @{self.tg_username or "N/A"})'
