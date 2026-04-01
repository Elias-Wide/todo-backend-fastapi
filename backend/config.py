from pathlib import Path
from typing import Literal, Optional

from cryptography.fernet import Fernet
from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.constants.core import (
    DEFAULT_JWT_ALGORITHM,
)

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'

STATIC_DIR = BASE_DIR / 'static'


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding='utf-8', extra='ignore'
    )


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='db_')

    host: str
    name: str
    password: SecretStr
    port: int
    user: str
    url: Optional[str] = Field(default=None)

    test_host: str = 'localhost'
    test_name: str = 'test_db'
    test_password: SecretStr = SecretStr('postgres')
    test_port: int = 5432
    test_user: str = 'postgres'
    test_url: Optional[str] = Field(default=None)

    @field_validator('url', mode='before')
    @classmethod
    def assemble_url(cls, v: Optional[str], info: ValidationInfo) -> str:
        if not v:
            return (
                f'postgresql+asyncpg://{info.data.get("user")}:'
                f'{info.data.get("password").get_secret_value()}@'
                f'{info.data.get("host")}:{info.data.get("port")}/'
                f'{info.data.get("name")}'
            )
        return v

    @field_validator('test_url', mode='before')
    @classmethod
    def assemble_test_url(cls, v: Optional[str], info: ValidationInfo) -> str:
        if not v:
            return (
                f'postgresql+asyncpg://{info.data.get("test_user")}:'
                f'{info.data.get("test_password").get_secret_value()}@'
                f'{info.data.get("test_host")}:{info.data.get("test_port")}/'
                f'{info.data.get("test_name")}'
            )
        return v


class AppConfig(ConfigBase):
    """
    Authentication and security settings for the application.

    Handles admin credentials and automated secret key generation
    using the 'APP_' environment prefix.
    """

    model_config = SettingsConfigDict(env_prefix='app_')
    mode: Literal['DEV', 'TEST', 'PROD']
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


class AIConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='ai_')
    api_key: str | None = None
    text_model: str | None = None
    speech_model: str | None = None


class UserAuthConfig(ConfigBase):
    """
    User authentication settings, including JWT configuration.
    """

    jwt_algorithm: str = Field(
        default=DEFAULT_JWT_ALGORITHM, alias='AUTH_JWT_ALGORITHM'
    )
    jwt_secret_key: str = Field(alias='AUTH_JWT_SECRET_KEY')
    access_token_expires_minutes: int = Field(
        default=15,
        alias='AUTH_ACCESS_TOKEN_EXPIRES_MINUTES',
    )
    refresh_token_expires_minutes: int = Field(
        default=60 * 24 * 30,
        alias='AUTH_REFRESH_TOKEN_EXPIRES_MINUTES',
    )
    session_ttl_minutes: int = Field(
        default=60 * 24,
        alias='AUTH_SESSION_TTL_MINUTES',
    )
    session_extend_minutes: int = Field(
        default=60 * 24 * 7,
        alias='AUTH_SESSION_EXTEND_MINUTES',
    )
    session_rolling_interval_minutes: int = Field(
        default=10,
        alias='AUTH_SESSION_ROLLING_INTERVAL_MINUTES',
    )
    session_absolute_timeout_days: int = Field(
        default=30,
        alias='AUTH_SESSION_ABSOLUTE_TIMEOUT_DAYS',
    )
    session_cookie_name: str = Field(
        default='session_id',
        alias='AUTH_SESSION_COOKIE_NAME',
    )
    session_cookie_secure: bool = Field(
        default=False,
        alias='AUTH_SESSION_COOKIE_SECURE',
    )
    session_cookie_domain: str | None = Field(
        default=None,
        alias='AUTH_SESSION_COOKIE_DOMAIN',
    )
    access_cookie_name: str = Field(
        default='access_token',
        alias='AUTH_ACCESS_COOKIE_NAME',
    )
    refresh_cookie_name: str = Field(
        default='refresh_token',
        alias='AUTH_REFRESH_COOKIE_NAME',
    )

    model_config = SettingsConfigDict(env_prefix='auth_')


class Settings(BaseSettings):
    """
    Global application settings container.

    Integrates database connection and authentication configurations.
    """

    app_name: str = 'Todo'
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    app: AppConfig = Field(default_factory=AppConfig)
    auth: UserAuthConfig = Field(default_factory=UserAuthConfig)
    ai: AIConfig = Field(default_factory=AIConfig)

    @classmethod
    def load(cls) -> 'Settings':
        """Initializes and returns a Settings instance."""
        return cls()


settings: Settings = Settings.load()
