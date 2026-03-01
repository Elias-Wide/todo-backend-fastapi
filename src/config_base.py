from pydantic import Field
from pathlib import Path
from typing import Optional
from pydantic import SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
print(f"BASE_DIR: {BASE_DIR}")
ENV_PATH = BASE_DIR / "infra" / ".env"


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    host: str
    name: str
    password: SecretStr
    port: int
    user: str
    url: Optional[str] = Field(default=None)

    @field_validator("url", mode="before")
    @classmethod
    def assemble_url(cls, v: Optional[str], info: ValidationInfo) -> str:
        if not v:
            pwd = info.data.get("password").get_secret_value()
            return (
                f"postgresql+asyncpg://{info.data.get('user')}:"
                f"{pwd}@{info.data.get('host')}:"
                f"{info.data.get('port')}/{info.data.get('name')}"
            )
        return v
