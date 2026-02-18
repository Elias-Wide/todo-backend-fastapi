from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet
from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.config_base import ConfigBase, DatabaseConfig

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / 'static'


class AuthConfig(ConfigBase):
    """
    Authentication and security settings for the application.

    Handles admin credentials and automated secret key generation
    using the 'APP_' environment prefix.
    """

    model_config = SettingsConfigDict(env_prefix='app_')
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


class Settings(BaseSettings):
    """
    Global application settings container.

    Integrates database connection and authentication configurations.
    """

    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)

    @classmethod
    def load(cls) -> 'Settings':
        """Initializes and returns a Settings instance."""
        return cls()


settings = Settings.load()
