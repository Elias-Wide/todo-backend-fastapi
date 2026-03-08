import pytest


@pytest.fixture
def valid_user_data():
    return {'username': 'valid_user', 'password': 'secret_password_123'}


@pytest.fixture
def invalid_user_data_short():
    return {'username': 'u', 'password': '1'}


@pytest.fixture
def user_data_missing_fields():
    return {'username': 'only_name'}
