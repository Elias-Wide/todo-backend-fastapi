from config import settings
class UserRoutes:
    """Endpoints for user management and authentication."""
    def __init__(self, base_url: str):
        self._base = f"{base_url}users"

    @property
    def register(self) -> str:
        return f"{self._base}/register"

    @property
    def login(self) -> str:
        return f"{self._base}/login"

    @property
    def logout(self) -> str:
        return f"{self._base}/logout"

    @property
    def refresh(self) -> str:
        return f"{self._base}/token/refresh"

    @property
    def me(self) -> str:
        return f"{self._base}/me"

class TaskRoutes:
    """Endpoints for tasks and AI integration."""
    def __init__(self, base_url: str):
        self._base = f"{base_url}tasks"

    @property
    def base(self) -> str:
        return self._base

    @property
    def send_ai(self) -> str:
        return f"{self._base}/send_ai_request"
    
    @property
    def delete(self, task_id: str | int) -> str:
        """Construct the URL for a specific task deletion."""
        return f"{self._base}/{task_id}"

class APIRoutes:
    """Centralized API v1 route management."""
    def __init__(self, api_url: str):
        self._v1 = f"{api_url.rstrip('/')}/api/v1/"
        self.users = UserRoutes(self._v1)
        self.tasks = TaskRoutes(self._v1)

api_routes = APIRoutes(settings.api_url)
