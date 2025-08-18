"""
Application entry point.

- Creates the FastAPI app.
- Configures lifespan events (startup/shutdown).
- Includes routers (e.g., /entries).
- Defines a basic health check endpoint.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from .database import Base, engine
from . import models #makes sure models are imported before create_all
from .routers import entries

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown (nothing for now)

app = FastAPI(lifespan=lifespan)

app.include_router(entries.router)

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"

