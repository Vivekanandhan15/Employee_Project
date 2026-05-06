from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.database import engine, Base, SessionLocal

from routers.user_router import router as user_router
from routers.department_router import router as department_router
from routers.user_department_router import router as user_department_router

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

@app.get("/")
def greet():
    return {"message":"Hello User"}


app.include_router(user_router)
app.include_router(department_router)
app.include_router(user_department_router)