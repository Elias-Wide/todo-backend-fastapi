from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from config_base import ConfigBase, DatabaseConfig


class TelegramConfig(ConfigBase):
    """
    Configuration settings for the Telegram Bot.

    Loads parameters with the 'TG_' prefix from environment variables.
    """

    model_config = SettingsConfigDict(env_prefix="tg_")

    bot_token: SecretStr
    admin_username: str
    admin_id: int
    webhook_host: str


class BotSettings(BaseSettings):
    """
    Main entry point for application settings.

    Combines database and Telegram configurations into a single schema.
    """

    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    tg: TelegramConfig = Field(default_factory=TelegramConfig)


bot_settings = BotSettings()
