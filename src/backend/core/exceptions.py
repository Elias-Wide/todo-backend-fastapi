class AppError(Exception):
    """Base application error."""


class RepositoryNotInitializedError(AppError):
    """Repository is not initialized in DBManager."""


class InvalidCredentialsError(AppError):
    """Invalid username/password pair."""


class UserAlreadyExistsError(AppError):
    """User already exists."""


class UserNotFoundError(AppError):
    """User not found."""


class RefreshTokenNotFoundError(AppError):
    """Refresh token not found or revoked."""


class RefreshTokenExpiredError(AppError):
    """Refresh token has expired."""
