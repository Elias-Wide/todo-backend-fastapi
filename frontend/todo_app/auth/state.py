import reflex as rx
import httpx
from config import settings
from frontend.todo_app.models.users import User
from routes import api_routes

class AuthState(rx.State):
    access_token: str = rx.Cookie(
        "",
        name=settings.auth.access_cookie_name,
        max_age=settings.auth.access_token_expires_minutes * 60
    )
    refresh_token: str = rx.Cookie(
        "",
        name=settings.auth.refresh_cookie_name,
        max_age=settings.auth.refresh_token_expires_minutes * 60
    )
    is_login: bool = True
    is_loading: bool = False
    logged_in: bool = False
    
    @rx.event
    async def check_user_token(self):
        if not self.access_token and not self.access_token:
            
    async def handle_submit(self, form_data: dict):
        self.is_loading = True
        yield
        if not self.user:
            yield rx.redirect("/login")
        if self.is_login:
            target_url = api_routes.users.login
        else:
            target_url = api_routes.users.register
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    target_url, 
                    json=form_data,
                    timeout=5.0
                )
            if target_url == api_routes.users.register and response.status_code == 201:
                yield rx.toast.success("Success")
                yield rx.redirect("/login")
            elif target_url == api_routes.users.login and response.status_code == 200:
                data = response.json() 
                self.access_token = data.get(f"{settings.auth.access_cookie_name}", "")
                self.refresh_token = data.get(f"{settings.auth.refresh_cookie_name}", "")
                yield rx.toast.success("Succeed LOGIN")
            else:
                error_data = response.json()
                error_msg = error_data.get("detail", "Error")
                yield rx.toast.error(f"Error: {error_msg}")

        except Exception as e:
            yield rx.toast.error(f"Cannot connect to the server: {str(e)}")
        
        finally:
            self.is_loading = False
            yield

    def toggle_auth_mode(self):
        self.is_login = not self.is_login