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
async def test_create_user(client: AsyncClient, user_data, expected_status):
    response = await client.post('/auth/register', json=user_data)

    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()['username'] == user_data['username']
