import importlib
import pkgutil
from pathlib import Path
from typing import List

from config_base import BASE_DIR
from fastapi import APIRouter, FastAPI

from src.core.base import BaseApiManager


class ApiManager(BaseApiManager):
    """
    Automated manager to discover and register FastAPI routers.

    This class scans a specified directory for Python modules, extracts
    APIRouter instances, and registers them to a FastAPI app instance.

    Attributes:
        routers_path (str): Package path to the directory containing routers.
        routers (list[APIRouter]): Collection of discovered router objects.
    """

    def __init__(
        self, routers_path: str = BASE_DIR / 'api' / 'routes'
    ):
        """
        Initialize the manager.

        Args:
            routers_path (str): Dot-separated path to the routers directory
                               (e.g., 'app.api.v1.routers').
        """
        if not hasattr(self, '_initialized'):
            self.routers_path: Path = routers_path
            self.routers: List[APIRouter] = []
            self._initialized = True

    def discover_routers(self):
        """
        Dynamically import modules and collect 'router' objects.

        Scans the directory defined in `routers_path`. It expects each
        module to have an attribute named 'router' which is an instance
        of fastapi.APIRouter.
        """
        if isinstance(self.routers_path, str):
            base_import_path = self.routers_path
            absolute_path = Path(base_import_path.replace('.', '/')).resolve()
        else:
            absolute_path = self.routers_path.resolve()

            try:
                parts = absolute_path.parts
                backend_index = parts.index('backend')
                base_import_path = '.'.join(parts[backend_index:])
            except ValueError:
                base_import_path = absolute_path.name

        if not absolute_path.exists():
            print(f'Directory not found: {absolute_path}')
            return
        for _, module_name, is_pkg in pkgutil.iter_modules(
            [str(absolute_path)]
        ):
            if is_pkg or module_name.startswith('_'):
                continue
            full_module_path = f'{base_import_path}.{module_name}'

            module = importlib.import_module(full_module_path)
            router = getattr(module, 'router', None)
            if isinstance(router, APIRouter):
                self.routers.append(router)

    def register_routes(self, app: FastAPI):
        """
        Register all discovered routers into the FastAPI app.

        Args:
            app (FastAPI): The target FastAPI application instance.
        """
        for router in self.routers:
            if router.include_in_schema:
                app.include_router(router)


api_mananger = ApiManager()
