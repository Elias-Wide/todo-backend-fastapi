from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    yield
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)
