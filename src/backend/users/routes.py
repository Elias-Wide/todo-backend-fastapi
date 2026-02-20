from typing import Annotated

from fastapi import APIRouter, Depends

from backend.users.schemas import SUserRegister

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/register')
def register_user(
    user: Annotated[SUserRegister, Depends()],
) -> SUserRegister: ...
