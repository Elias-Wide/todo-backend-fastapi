import httpx
import reflex as rx
from config import settings
from todo_app.auth.state import AuthState
from routes import api_routes

                
class TasksState(AuthState):
    tasks: list[] = []

    @rx.event
    async def fetch_tasks(self):
        if not self.auth_token:
            return rx.redirect("/login")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    api_routes.tasks.base, 
                    headers={"Authorization": f"Bearer {self.auth_token}"},
                )
                if response.status_code == 200:
                    self.tasks = response.json()
                elif response.status_code == 401:
                    return rx.redirect("/login")
                else:
                    yield rx.window_alert(f"Ошибка API: {response.status_code}")
                    
            except Exception as e:
                yield rx.window_alert(f"Ошибка соединения: {str(e)}")

def tasks_page():
    return rx.container(
        rx.grid(
            rx.foreach(
                TasksState.tasks,
                lambda item: rx.card(
                    rx.vstack(
                        rx.heading(item[0], size="3"), # Ключ (день недели)
                        rx.divider(),
                        rx.vstack(
                            rx.foreach(item[1], rx.text), # Список задач
                            align_items="start",
                        ),
                    ),
                )
            ),
            columns="5",
            spacing="4",
        ),
        on_mount=TasksState.fetch_tasks # Загрузка при входе на страницу
    )               