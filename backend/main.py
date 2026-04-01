from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from api.endpoints.v1.api_v1 import api_v1_router as main_router
from core.admin.admin_view import admin_views
from core.admin.auth import authentication_backend
from db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_system_prompt()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix='/api')
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)

for view in admin_views:
    admin.add_view(view)
