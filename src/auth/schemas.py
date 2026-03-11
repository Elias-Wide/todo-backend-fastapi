from pydantic import BaseModel, Field

from src.config import settings


class SJWTPayload(BaseModel):
    """Schema for JWT payload validation."""

    sub: str
    type: str
    iat: int
    exp: int
    iss: str = Field(default=settings.app.name)


class STokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class SLoginRequest(BaseModel):
    name: str = Field(..., example='johndoe')
    password: str = Field(..., example='strongpassword123')


class SRefreshRequest(BaseModel):
    refresh_token: str = Field(..., example='fdfdfb12wfvfc')
