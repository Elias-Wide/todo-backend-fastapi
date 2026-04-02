import reflex as rx

from todo_app.auth.views import auth_page




app = rx.App()
app.add_page(auth_page, route="/login")