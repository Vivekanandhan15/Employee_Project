from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse

from database.database import Base, engine, SessionLocal
from middleware.auth_middleware import JWTMiddleware

# Routers
from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.department_router import router as department_router
from routers.user_department_router import router as user_department_router
from routers.address_router import router as address_router

# Seeds
from seeds.department_seed import seed_departments


# Create all tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):

    db = SessionLocal()

    try:
        # Seed predefined departments
        seed_departments(db)

    finally:
        db.close()

    yield


app = FastAPI(
    title="User Department API",
    version="1.0.0",
    lifespan=lifespan
)

# Add JWT Middleware for global authentication
app.add_middleware(JWTMiddleware)


# Global Exception Handler
@app.exception_handler(Exception)
async def internal_server_error_handler(
    request: Request,
    exc: Exception
):

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

    return {
        "message": "Backend is running successfully"
    }


# Include Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(department_router)
app.include_router(user_department_router)
app.include_router(address_router)
@app.exception_handler(Exception)
async def internal_server_error_handler(
    request: Request,
    exc: Exception
):

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

    return {
        "message": "Backend is running successfully"
    }


# Include Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(department_router)
app.include_router(user_department_router)
app.include_router(address_router)