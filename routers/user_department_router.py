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
def assign_users_departments(
    payload: AssignDepartmentSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserDepartmentService.assign_users_departments(payload, db)


@router.get("/user/{user_id}")
def get_user_departments(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserDepartmentService.get_user_departments(
        user_id,
        db
    )


@router.get("/department/{dept_id}")
def get_department_users(
    dept_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserDepartmentService.get_department_users(
        dept_id,
        db
    )


@router.delete("/{user_id}/{dept_id}")
def remove_user_from_department(
    user_id: str,
    dept_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserDepartmentService.remove_user_from_department(
        user_id,
        dept_id,
        db
    )