class AppError(Exception):
    """Base application error."""

    msg = 'An unexpected application error occurred.'

    def __init__(self, message: str = None):
        super().__init__(message or self.msg)
        if message:
            self.msg = message

    def __str__(self):
        return self.msg


class AccessDeniedError(AppError):
    msg = 'Access denied: You are not the owner of this task'


class RepositoryNotInitializedError(AppError):
    """Repository is not initialized in DBManager."""

    msg = 'Database repository has not been initialized in DBManager.'


class InvalidCredentialsError(AppError):
    """Invalid username/password pair."""

    msg = 'Invalid username or password provided.'


class UserAlreadyExistsError(AppError):
    """User already exists."""

    msg = 'A user with this identifier already exists in the system.'


class UserNotFoundError(AppError):
    """User not found."""

    msg = 'The requested user could not be found.'


class RefreshTokenNotFoundError(AppError):
    """Refresh token not found or revoked."""

    msg = 'Refresh token is missing, invalid, or has been revoked.'


class RefreshTokenExpiredError(AppError):
    """Refresh token has expired."""

    msg = 'Refresh token has expired. Please log in again.'


class TaskNotFoundError(AppError):
    msg = 'Task with this id not found'


class AiResponseError(AppError):
    msg = 'Cannot define task from response'
