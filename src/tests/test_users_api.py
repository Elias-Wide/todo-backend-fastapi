import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


@pytest.mark.asyncio(loop_scope='session')
class TestUserRegistration:
    """Tests for user account creation and data validation."""

    @pytest.mark.parametrize(
        'user_data, expected_status',
        [
            (lf('valid_user_data'), 201),
            (lf('invalid_user_data_short'), 422),
            (lf('user_data_missing_fields'), 422),
        ],
    )
    async def test_create_user(
        self,
        client: AsyncClient,
        user_data,
        expected_status,
        user_register_route,
    ):
        """Verify user registration with valid and invalid data."""
        response = await client.post(user_register_route, json=user_data)

        assert response.status_code == expected_status
        if expected_status == 201:
            assert response.json()['username'] == user_data['username']


@pytest.mark.asyncio(loop_scope='session')
class TestUserAuthentication:
    """Tests for login process and token issuance."""

    async def test_authenticate_user(
        self,
        client: AsyncClient,
        registered_user,
        valid_user_data: dict,
        user_login_route: str,
    ):
        """Verify successful login returns access and refresh tokens."""
        response = await client.post(user_login_route, json=valid_user_data)

        assert response.status_code == 200
        data = response.json()
        assert data.get('access_token') is not None
        assert data.get('refresh_token') is not None

    async def test_authenticate_user_wrong_password(
        self,
        client: AsyncClient,
        registered_user,
        valid_user_data: dict,
        user_login_route: str,
    ):
        """Verify 401 error on incorrect password."""
        invalid_data = valid_user_data.copy()
        invalid_data['password'] = 'wrong_password_123'

        response = await client.post(user_login_route, json=invalid_data)
        assert response.status_code == 401

    async def test_authenticate_user_missing_fields(
        self,
        client: AsyncClient,
        user_data_missing_fields: dict,
        user_login_route: str,
    ):
        """Verify 422 error when required fields are missing in login request."""
        response = await client.post(
            user_login_route, json=user_data_missing_fields
        )

        assert response.status_code == 422
        assert response.json().get('detail') is not None
