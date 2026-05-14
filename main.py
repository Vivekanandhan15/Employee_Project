"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse

from database.database import Base, engine, SessionLocal, ensure_db_schema
from middleware.auth_middleware import JWTMiddleware

# Routers
from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.department_router import router as department_router
from routers.user_department_router import router as user_department_router
from routers.address_router import router as address_router
from routers.test_router import router as test_router
from routers.cache_router import router as cache_router

# Seeds
from seeds.department_seed import seed_departments

from services.background_sync_service import background_sync


# Create all tables and ensure schema upgrades
Base.metadata.create_all(bind=engine)
ensure_db_schema()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Application lifespan events."""

    db = SessionLocal()

    try:
        # Seed predefined departments
        seed_departments(db)

    finally:
        db.close()

    # Start background sync service
    background_sync.start()

    yield

    # Stop background sync service on shutdown
    background_sync.stop()


app = FastAPI(
    title="User Department API",
    version="1.0.0",
    lifespan=lifespan
)

# Add JWT Middleware for global authentication
app.add_middleware(JWTMiddleware)


@app.exception_handler(Exception)
async def internal_server_error_handler(
    _: Request,
    exc: Exception
):
    """Handle global application exceptions."""

    if isinstance(exc, HTTPException):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail
            }
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error"
        }
    )


@app.get("/")
def greet():
    """Health check endpoint."""

    return {
        "message": "Backend is running successfully"
    }


# Include Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(department_router)
app.include_router(user_department_router)
app.include_router(address_router)
app.include_router(test_router)
app.include_router(cache_router)