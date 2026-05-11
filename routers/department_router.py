from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth_dependency import get_current_user
from schemas.department_schema import DepartmentCreate, DepartmentResponse
from services.department_service import DepartmentService

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return DepartmentService.create_department(payload, db)


@router.get("/", response_model=List[DepartmentResponse])
def get_all_departments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return DepartmentService.get_all_departments(db)


@router.get("/{dept_id}", response_model=DepartmentResponse)
def get_department_by_id(
    dept_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return DepartmentService.get_department_by_id(dept_id, db)


@router.put("/{dept_id}")
def update_department(
    dept_id: str,
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return DepartmentService.update_department(
        dept_id,
        payload,
        db
    )


@router.delete("/{dept_id}")
def delete_department(
    dept_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return DepartmentService.delete_department(dept_id, db)