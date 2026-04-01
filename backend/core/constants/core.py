from enum import StrEnum

DEFAULT_JWT_ALGORITHM: str = 'HS246'
DEFAULT_ACCESS_TOKEN_EXPIRES_MIN: int = 15
DEFAULT_REFRESH_TOKEN_EXPIRES_MIN: int = 10080
MAIN_API_ROUTE: str = '/api/v1'


class AppLang(StrEnum):
    RU: str = 'russian'
