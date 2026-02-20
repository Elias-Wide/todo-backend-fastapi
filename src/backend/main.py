from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.db.database import create_tables, drop_tables
from backend.tasks.routes import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await drop_tables()


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
