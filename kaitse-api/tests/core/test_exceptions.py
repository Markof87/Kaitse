from httpx import AsyncClient, ASGITransport

import pytest
from fastapi import FastAPI

from app.core.exceptions import register_exception_handlers
from app.domain.exceptions import NotFoundError, ValidationError, ConflictError

async def test_not_found_exception_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise NotFoundError("Player", "123")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/test")

    assert r.status_code == 404

async def test_validation_exception_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise ValidationError("Player","Invalid input")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/test")

    assert r.status_code == 422
    assert "Validation error" in r.json()["detail"]

async def test_conflict_exception_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise ConflictError("Player", "slug", "mario-rossi")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/test")

    assert r.status_code == 409
    assert "already exists" in r.json()["detail"]