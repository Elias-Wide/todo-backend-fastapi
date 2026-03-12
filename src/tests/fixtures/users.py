import pytest

from src.db.db_manager import DBManager
from src.users.schemas import SUserRegister
from src.users.services import UsersService


@pytest.fixture
def user_register_route(main_api_route) -> str:
    return main_api_route + '/users/register'


@pytest.fixture
def user_login_route(main_api_route) -> str:
    return main_api_route + '/users/login'


@pytest.fixture
def valid_user_data():
    return {'username': 'valid_user', 'password': 'secret_password_123'}


@pytest.fixture
def invalid_user_data_short():
    return {'username': 'u', 'password': '1'}


@pytest.fixture
def user_data_missing_fields():
    return {'username': 'only_name'}


@pytest.fixture(scope='function')
async def registered_user(db_session: DBManager, valid_user_data: dict):
    service = UsersService(db_session)
    user = await service.get_user_profile(valid_user_data['username'])
    return (
        user
        if user
        else await service.register_user(SUserRegister(**valid_user_data))
    )
