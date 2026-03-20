from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.endpoints.v1.api_v1 import api_v1_router as main_router
from src.services.ai.utils import create_system_prompt


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_system_prompt()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix='/api')
