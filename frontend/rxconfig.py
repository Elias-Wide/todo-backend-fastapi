import reflex as rx
from config import settings
config = rx.Config(
    app_name="todo_app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    backend_port=8888
)