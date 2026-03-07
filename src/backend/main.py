from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.services import ApiManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
api_manager: ApiManager = ApiManager()
api_manager.discover_routers()
api_manager.register_routes(app)
