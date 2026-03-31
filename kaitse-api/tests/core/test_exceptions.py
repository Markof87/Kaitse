import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.core.exceptions import register_exception_handlers
from app.domain.exceptions import NotFoundError, ValidationError, ConflictError

def test_not_found_exception_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise NotFoundError("Player", "123")

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_validation_exception_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise ValidationError("Player","Invalid input")

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 422
    assert "Validation error" in response.json()["detail"]

def test_conflict_exception_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise ConflictError("Player", "slug", "mario-rossi")

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]