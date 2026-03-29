from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import NotFoundError, ValidationError, ConflictError, DomainError, IntegrityError

def register_exception_handlers(app: FastAPI) -> None:

    """Registers global exception handlers for the FastAPI application."""

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.detail, "data": exc.data})
    
    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.detail, "data": exc.data})
    
    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.detail, "data": exc.data})
    
    @app.exception_handler(IntegrityError)
    async def integrity_handler(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.detail, "data": exc.data})
    
    @app.exception_handler(DomainError)
    async def domain_handler(request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": exc.detail, "data": exc.data})