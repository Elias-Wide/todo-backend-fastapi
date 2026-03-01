from typing import Annotated, AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.db.database import SessionLocal, get_session
from backend.db.db_manager import DBManager
from backend.users.models import UsersOrm
from backend.users.schemas import SUser
from backend.users.services import UsersService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_db_manager() -> AsyncGenerator[DBManager, None]:
    async with DBManager(SessionLocal) as manager:
        yield manager


DBManagerDep = Annotated[DBManager, Depends(get_db_manager)]


async def get_current_user(
    request: Request,
    db: DBManagerDep,
) -> SUser:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token missing',
        )
    try:
        payload = jwt.decode(
            token,
            settings.auth.jwt_secret_key,
            algorithms=[settings.auth.jwt_algorithm],
        )
        user_id: str = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
        ) from e
    service = UsersService(db)
    user = await service.get_user_profile('id', int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
        )
    return user


UserDep = Annotated[UsersOrm, Depends(get_current_user)]
