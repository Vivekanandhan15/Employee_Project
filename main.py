from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from database.database import engine, Base, SessionLocal

from routers.user_router import router as user_router
from routers.department_router import router as department_router
from routers.user_department_router import router as user_department_router
from routers.address_router import router as address_router

from seeds.department_seed import seed_departments

from models.user import User
from models.department import Department

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    db = SessionLocal()

    try:
        seed_departments(db)

    finally:
        db.close()  

    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

@app.get("/")
def greet():
    return {"BACKEND IS RUNNING SUCCESSFULLY": "Welcome to the User-Department API!"}


app.include_router(user_router)
app.include_router(department_router)
app.include_router(user_department_router)
app.include_router(address_router)

