import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def tasks_route(main_api_route: str) -> str:
    """Base route for tasks endpoints."""
    return f'{main_api_route}/tasks'


@pytest.fixture
def random_task_data():
    """Fixture for generating random task data using Faker."""
    return {
        'title': fake.sentence(nb_words=3).rstrip('.'),
        'description': fake.paragraph(nb_sentences=2),
        'is_daily': fake.boolean(),
        'scheduled_time': fake.date_time_between(
            start_date='now', end_date='+30d'
        ),
    }
