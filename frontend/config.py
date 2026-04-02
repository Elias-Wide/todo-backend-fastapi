from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

ENV_PATH: str = ".env"

class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, 
        env_file_encoding='utf-8', 
        extra='ignore'
    )

class AuthConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='auth_')
    
    jwt_algorithm: str = "HS256"
    jwt_secret_key: str = "default_secret"
    
    access_token_expires_minutes: int = 15
    refresh_token_expires_minutes: int = 43200
    
    session_ttl_minutes: int = 1440
    session_extend_minutes: int = 10080
    session_rolling_interval_minutes: int = 10
    session_absolute_timeout_days: int = 30
    
    session_cookie_name: str = "session_id"
    session_cookie_secure: bool = False
    session_cookie_domain: str = ""
    
    access_cookie_name: str = "todo_access_token"
    refresh_cookie_name: str = "todo_refresh_token"

class Settings(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='frontend_')
    
    app_name: str = "PureDo"
    api_url: str = "http://localhost:8000/"
    auth: AuthConfig = Field(default_factory=AuthConfig)

    @classmethod
    def load(cls) -> 'Settings':
        """Initializes and returns a Settings instance."""
        return cls()

settings = Settings()
