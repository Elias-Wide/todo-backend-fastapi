from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from backend.api.dependecies import DBManagerDep
from backend.auth.schemas import SLoginRequest, SRefreshRequest, STokenPair
from backend.auth.services import AuthServiceJWT
from backend.core.config import settings
from backend.core.exceptions import (
    AppError,
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from backend.users.schemas import SUser, SUserRegister
from backend.users.services import UsersService

router = APIRouter(prefix='/users', tags=['users'])


def _set_token_cookies(
    response: Response, access_token: str, refresh_token: str
) -> None:
    """Set access and refresh tokens in HTTP-only cookies."""
    response.set_cookie(
        key=settings.auth.access_cookie_name,
        value=access_token,
        httponly=False,
        secure=settings.auth.session_cookie_secure,
        samesite='lax',
        max_age=settings.auth.access_token_expires_minutes * 60,
        domain=settings.auth.session_cookie_domain,
        path='/',
    )
    response.set_cookie(
        key=settings.auth.refresh_cookie_name,
        value=refresh_token,
        httponly=False,
        secure=settings.auth.session_cookie_secure,
        samesite='lax',
        max_age=settings.auth.refresh_token_expires_minutes * 60,
        domain=settings.auth.session_cookie_domain,
        path='/',
    )


@router.post('/register')
async def register_user(
    user_data: Annotated[SUserRegister, Depends()],
    db: DBManagerDep,
) -> SUser:
    """Register a new user and return the user data."""
    service = UsersService(db)
    try:
        return await service.register_user(user_data)
    except UserAlreadyExistsError as err:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@router.post('/login', summary='Authenticate user and obtain JWT tokens')
async def login(
    data: Annotated[SLoginRequest, Depends()],
    db: DBManagerDep,
    response: Response,
) -> STokenPair:
    """Authenticate user and set JWT tokens in cookies."""
    jwt_service = AuthServiceJWT(db)
    try:
        access_token, refresh_token = await jwt_service.login(
            data.name, data.password
        )
    except InvalidCredentialsError as err:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=str(err)
        ) from err
    except AppError as err:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    _set_token_cookies(response, access_token, refresh_token)
    return STokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    '/token/refresh', summary='Refresh JWT tokens using a refresh token'
)
async def refresh_tokens(
    data: SRefreshRequest, response: Response, db: DBManagerDep
) -> STokenPair:
    """Refresh session tokens and update cookies using a refresh token."""
    jwt_service = AuthServiceJWT(db)
    try:
        pair = await jwt_service.refresh(data.refresh_token)
    except RefreshTokenExpiredError as err:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=str(err)
        ) from err
    except RefreshTokenNotFoundError as err:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=str(err)
        ) from err
    except UserNotFoundError as err:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=str(err)
        ) from err
    except AppError as err:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    _set_token_cookies(response, pair.access_token, pair.refresh_token)
    return pair
