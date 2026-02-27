import secrets
from datetime import datetime, timedelta, timezone

from jwt import jwt
from jwt.exceptions import InvalidKeyTypeError

from backend.auth.schemas import JWTPayload
from backend.core.config import settings


class TokenHelper:
    def create_access_token(self, user_id: int) -> str:
        """Create JWT access token with expiration from settings."""
        return self._create_token(
            user_id, 'access', settings.auth.access_token_expires_minutes
        )

    def create_refresh_token(self) -> str:
        """Generate a long-lived random refresh token string."""
        return secrets.token_urlsafe(48)

    def decode_token(
        self, token: str, expected_type: str, iss: str = settings.app.name
    ) -> JWTPayload:
        """Decode JWT and validate structure using JWTPayload schema."""
        raw_payload = jwt.decode(
            token,
            settings.auth.jwt_secret_key,
            algorithms=[settings.auth.jwt_algorithm],
            issuer=iss,
        )
        payload = JWTPayload(**raw_payload)

        if payload.type != expected_type:
            raise InvalidKeyTypeError('Invalid token type')

        return payload

    def _create_token(
        self,
        user_id: int,
        token_type: str,
        expires_minutes: int,
        iss: str = settings.app.name,
    ) -> str:
        """Assemble JWT with specific type, sub, and expiration."""
        now = datetime.now(timezone.utc)
        payload = {
            'sub': str(user_id),
            'type': token_type,
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(minutes=expires_minutes)).timestamp()),
            'iss': iss,
        }
        return jwt.encode(
            payload,
            settings.auth.jwt_secret_key,
            algorithm=settings.auth.jwt_algorithm,
        )


tokens = TokenHelper()
