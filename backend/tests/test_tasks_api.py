import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio(loop_scope='session')
class TestTasksApi:
    """Tests for authorized task operations (CRUD)."""

    async def test_add_task_success(
        self,
        client_with_user: AsyncClient,
        tasks_route: str,
        random_task_data: dict,
    ):
        """Test creating a task. Uses params because of Depends() in router."""
        response = await client_with_user.post(
            tasks_route, params=random_task_data
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'id' in data
        assert isinstance(data['id'], int)

    async def test_get_tasks_list(
        self,
        client_with_user: AsyncClient,
        tasks_route: str,
        random_task_data: dict,
    ):
        """Test retrieving tasks for the current mocked user."""
        # 1. Create a task via API
        await client_with_user.post(tasks_route, params=random_task_data)

        # 2. Get the list
        response = await client_with_user.get(tasks_route)

        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) > 0
        assert tasks[0]['title'] == random_task_data['title']

    async def test_delete_task_success(
        self,
        client_with_user: AsyncClient,
        tasks_route: str,
        random_task_data: dict,
    ):
        """Test successful task deletion."""
        # 1. Create
        post_res = await client_with_user.post(
            tasks_route, params=random_task_data
        )
        task_id = post_res.json()['id']

        # 2. Delete
        delete_res = await client_with_user.delete(f'{tasks_route}/{task_id}')
        assert delete_res.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verify it is gone
        get_res = await client_with_user.get(tasks_route)
        assert not any(t['id'] == task_id for t in get_res.json())

    async def test_delete_task_not_found(
        self, client_with_user: AsyncClient, tasks_route: str
    ):
        """Test 404 error when deleting non-existent task."""
        invalid_id = 99999
        response = await client_with_user.delete(f'{tasks_route}/{invalid_id}')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'detail' in response.json()


@pytest.mark.asyncio(loop_scope='session')
class TestTasksSecurity:
    """Tests for unauthorized access and security checks."""

    async def test_get_tasks_unauthorized(
        self, client: AsyncClient, tasks_route: str
    ):
        """Expect 401 when trying to get tasks without a token."""
        response = await client.get(tasks_route)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == 'Token missing'

    async def test_add_task_unauthorized(
        self, client: AsyncClient, tasks_route: str, random_task_data: dict
    ):
        """Expect 401 when trying to add a task without a token."""
        response = await client.post(tasks_route, params=random_task_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == 'Token missing'

    async def test_delete_task_unauthorized(
        self, client: AsyncClient, tasks_route: str
    ):
        """Expect 401 when trying to delete a task without a token."""
        response = await client.delete(f'{tasks_route}/1')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == 'Token missing'

    async def test_invalid_token_format(
        self, client: AsyncClient, tasks_route: str
    ):
        """Expect 401 when the token cookie exists but is invalid."""
        client.cookies.set('access_token', 'not-a-real-jwt-token')

        response = await client.get(tasks_route)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == 'Invalid token'
