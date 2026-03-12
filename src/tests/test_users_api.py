import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'user_data, expected_status',
    [
        (lf('valid_user_data'), 201),
        (lf('invalid_user_data_short'), 422),
        (lf('user_data_missing_fields'), 422),
    ],
)
async def test_create_user(
    client: AsyncClient, user_data, expected_status, user_register_route
):
    response = await client.post(user_register_route, json=user_data)

    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()['username'] == user_data['username']


@pytest.mark.asyncio
async def test_authenticate_user(
    client: AsyncClient,
    create_user,
    valid_user_data: dict[str],
    user_login_route: str,
):
    response = await client.post(user_login_route, json=valid_user_data)
    assert response.status_code == 200
    assert response.json().get('access_token', None) is not None
    assert response.json().get('refresh_token', None) is not None


async def test_authenticate_user_wrong_password(
    client: AsyncClient,
    create_user,
    valid_user_data: dict,
    user_login_route: str,
):
    invalid_data = valid_user_data.copy()
    invalid_data['password'] = 'wrong_password_123'
    response = await client.post(user_login_route, json=invalid_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_authenticate_user_missing_fields(
    client: AsyncClient, user_data_missing_fields: dict, user_login_route: str
):
    response = await client.post(
        user_login_route, json=user_data_missing_fields
    )

    assert response.status_code == 422
    errors = response.json().get('detail')
    assert errors is not None
