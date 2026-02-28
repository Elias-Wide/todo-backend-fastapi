from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.services import ApiManager
from backend.db.database import create_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await drop_tables()


app = FastAPI(lifespan=lifespan)
api_manager: ApiManager = ApiManager()
api_manager.discover_routers()
api_manager.register_routes(app)
