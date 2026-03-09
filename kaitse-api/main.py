from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import get_logger, setup_logging

# Initialize logging
setup_logging()

logger = get_logger(__name__)

#Manage application lifecycle events
#code before 'yield' runs on startup, code after 'yield' runs on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Kaitse API Starting", env=settings.app_env, debug=settings.debug)
    # Perform any startup tasks here (e.g., connect to databases, initialize resources)
    yield
    logger.info("Kaitse API Shutting down")
    # Perform any cleanup tasks here (e.g., close database connections, release resources)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        description="API for football data management",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.app_env=="development" else None,
        redoc_url="/redoc" if settings.app_env=="development" else None,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.app_env=="development" else [],  # Adjust this in production to restrict origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #HEALTH CHECK ENDPOINT - minimum endpoint to verify that the API is up and running
    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "env": settings.app_env}

    # Import and include API routes
    #from app.api import api_router
    #app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app

app = create_app()