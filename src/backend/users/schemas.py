from pydantic import BaseModel, ConfigDict, Field

from backend.users.constants import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)


class SUser(BaseModel):
    """
    Schema for representing a user in the system. This model includes
    essential user information such as username, email, and password.
    It also provides validation rules for each field to ensure data integrity.
    """

    id: int
    username: str = Field(
        ..., min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH
    )
    tg_id: int | None = Field(
        default=None, description='Telegram ID of the user'
    )
    model_config = ConfigDict(from_attributes=True)


class SUserRegister(BaseModel):
    """
    Schema for representing a user in the system. This model includes
    essential user information such as username, email, and password.
    It also provides validation rules for each field to ensure data integrity.
    """

    username: str = Field(
        ..., min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH
    )
    password: str = Field(
        ..., min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )
    model_config = ConfigDict(from_attributes=True)


class SUserLogin(BaseModel):
    """
    Schema for user login.
    This model includes the username and password fields,
    which are required for authenticating a user. The validation rules ensure
    that the username and password meet the specified length requirements.
    """

    username: str = Field(
        ..., min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH
    )
    password: str = Field(
        ..., min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )
    model_config = ConfigDict(from_attributes=True)
