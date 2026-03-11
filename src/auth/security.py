import hashlib

import bcrypt

from src.core.base import BaseSecurity


class Security(BaseSecurity):
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt with a SHA-256 pre-hash."""
        digest = self._password_digest(password)
        return bcrypt.hashpw(digest, bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password by comparing it with the stored bcrypt hash."""
        digest = self._password_digest(password)
        return bcrypt.checkpw(digest, password_hash.encode('utf-8'))

    def _password_digest(self, password: str) -> bytes:
        """Create SHA-256 digest to bypass bcrypt's length limitation."""
        return hashlib.sha256(password.encode('utf-8')).digest()


security = Security()
