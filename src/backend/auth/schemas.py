from pydantic import BaseModel, Field

from backend.core.config import settings


class JWTPayload(BaseModel):
    """Schema for JWT payload validation."""

    sub: str
    type: str
    iat: int
    exp: int
    iss: str = Field(default=settings.app.name)
