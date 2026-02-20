from typing import Optional

from config_base import BASE_DIR, ConfigBase, DatabaseConfig
from cryptography.fernet import Fernet
from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.constants import (
    DEFAULT_ACCESS_TOKEN_EXPIRES_MIN,
    DEFAULT_JWT_ALGORITHM,
    DEFAULT_REFRESH_TOKEN_EXPIRES_MIN,
)

BACKEND_DIR = BASE_DIR / 'src' / 'backend'
STATIC_DIR = BASE_DIR / 'src' / 'static'


class AppAuthConfig(ConfigBase):
    """
    Authentication and security settings for the application.

    Handles admin credentials and automated secret key generation
    using the 'APP_' environment prefix.
    """

    model_config = SettingsConfigDict(env_prefix='app_')
    name: str = 'ToDo'
    logging_mode: str = 'on'
    admin_email: str
    admin_password: SecretStr
    admin_sc: SecretStr
    secret_key: Optional[SecretStr] = Field(default=None)

    @field_validator('secret_key', mode='before')
    @classmethod
    def assemble_secret_key(
        cls, v: Optional[str], values: ValidationInfo
    ) -> str:
        """
        Generates a new Fernet key if 'secret_key' is not provided in env.
        """
        return v or Fernet.generate_key().decode()

    def refresh_secret_key(self):
        """Rotates the secret key by generating a fresh Fernet token."""
        self.secret_key = Fernet.generate_key()


class UserAuthConfig(ConfigBase):
    """
    User authentication settings, including JWT configuration.
    """

    jwt_algorithm: str = Field(
        default=DEFAULT_JWT_ALGORITHM, alias='AUTH_JWT_ALGORITHM'
    )
    jwt_secret_key: str = Field(
        default='change-me', alias='AUTH_JWT_SECRET_KEY'
    )
    access_token_expires_minutes: int = Field(
        default=DEFAULT_ACCESS_TOKEN_EXPIRES_MIN,
        alias='AUTH_ACCESS_TOKEN_EXPIRES_MINUTES',
    )
    refresh_token_expires_minutes: int = Field(
        default=DEFAULT_REFRESH_TOKEN_EXPIRES_MIN,
        alias='AUTH_REFRESH_TOKEN_EXPIRES_MINUTES',
    )
    model_config = SettingsConfigDict(env_prefix='auth_')


class Settings(BaseSettings):
    """
    Global application settings container.

    Integrates database connection and authentication configurations.
    """

    app_name: str = 'Todo'
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    app: AppAuthConfig = Field(default_factory=AppAuthConfig)
    auth: UserAuthConfig = Field(default_factory=UserAuthConfig)

    @classmethod
    def load(cls) -> 'Settings':
        """Initializes and returns a Settings instance."""
        return cls()


settings: Settings = Settings.load()
