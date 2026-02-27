from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.routes.tasks import router as tasks_router
from backend.db.database import create_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await drop_tables()


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
