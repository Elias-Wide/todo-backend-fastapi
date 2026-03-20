import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from src.config import settings
from src.schemas.tokens import SJWTPayload


class TokenHelper:
    def __init__(self):
        self.algorithm = settings.auth.jwt_algorithm
        self.secret = settings.auth.jwt_secret_key

    def create_access_token(self, user_id: int) -> str:
        """Create JWT access token with expiration from settings."""
        return self._create_token(
            user_id, 'access', settings.auth.access_token_expires_minutes
        )

    def create_refresh_token(self) -> str:
        """Generate a long-lived random refresh token string."""
        return secrets.token_urlsafe(48)

    def hash_token(self, token: str) -> str:
        """Hash a token string for secure storage and comparison."""
        return hashlib.sha256(token.encode('utf-8')).hexdigest()

    def decode_token(
        self,
        encoded_token: str,
        expected_type: str,
        iss: str = settings.app.name,
    ) -> SJWTPayload:
        """Decode JWT and validate structure using JWTPayload schema."""
        raw_payload = jwt.decode(
            encoded_token,
            self.secret,
            algorithms=[self.algorithm],
            issuer=iss,
        )
        payload = SJWTPayload(**raw_payload)

        if payload.type != expected_type:
            raise InvalidTokenError('Invalid token type')

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
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)


tokens = TokenHelper()


@dataclass
class BaseCookie:
    """
    Base configuration for JWT cookies used in authentication.

    Centralizes common cookie attributes to ensure consistency between
    Access and Refresh tokens.
    """

    httponly: bool = True
    secure: bool = settings.auth.session_cookie_secure
    samesite: str = 'lax'
    domain: str = settings.auth.session_cookie_domain
    path: str = '/'

    def get_set_params(
        self, key: str, value: str, max_age_minutes: int
    ) -> dict:
        """
        Generates a full set of parameters for the response.set_cookie method.

        Args:
            key: The name of the cookie.
            value: The token string to store.
            max_age_minutes: Expiration time in minutes (converted to seconds).

        Returns:
            A dictionary of keyword arguments for response.set_cookie.
        """
        return {
            'key': key,
            'value': value,
            'httponly': self.httponly,
            'secure': self.secure,
            'samesite': self.samesite,
            'domain': self.domain,
            'path': self.path,
            'max_age': max_age_minutes * 60,
        }

    def get_delete_params(self, key: str) -> dict:
        """
        Generates parameters for the response.delete_cookie method.

        Ensures that the cookie is deleted using the same domain and path
        it was created with.
        """
        return {
            'key': key,
            'httponly': self.httponly,
            'secure': self.secure,
            'samesite': self.samesite,
            'domain': self.domain,
            'path': self.path,
        }


def get_cookie_config() -> BaseCookie:
    return BaseCookie()
