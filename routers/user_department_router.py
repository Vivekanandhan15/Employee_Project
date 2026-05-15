from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth_dependency import get_current_user
from schemas.user_department_schema import AssignDepartmentSchema
from services.user_department_service import UserDepartmentService

router = APIRouter(
    prefix="/user-departments",
    tags=["User Departments"]
)


@router.post("/")
async def assign_users_departments(
    payload: AssignDepartmentSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserDepartmentService.assign_users_departments(payload, db)


@router.get("/user/{user_id}")
async def get_user_departments(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserDepartmentService.get_user_departments(
        user_id,
        db
    )


@router.get("/department/{dept_id}")
async def get_department_users(
    dept_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserDepartmentService.get_department_users(
        dept_id,
        db
    )


@router.delete("/{user_id}/{dept_id}")
async def remove_user_from_department(
    user_id: str,
    dept_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserDepartmentService.remove_user_from_department(
        user_id,
        dept_id,
        db
    )