from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt import PyJWTError

from src.config import settings
from src.dependencies.db_manager import DBManagerDep
from src.models.users import UsersOrm
from src.schemas.users import SUser
from src.services.users import UsersService


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
    user = await service.get_user_profile(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
        )
    return user


UserDep = Annotated[UsersOrm, Depends(get_current_user)]
