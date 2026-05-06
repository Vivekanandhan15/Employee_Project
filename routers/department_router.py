from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.department_schema import DepartmentCreate
from services.department_service import DepartmentService

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post("/")
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db)
):
    return DepartmentService.create_department(payload, db)


@router.get("/")
def get_all_departments(
    db: Session = Depends(get_db)
):
    return DepartmentService.get_all_departments(db)


@router.get("/{dept_id}")
def get_department_by_id(
    dept_id: str,
    db: Session = Depends(get_db)
):
    return DepartmentService.get_department_by_id(dept_id, db)


@router.put("/{dept_id}")
def update_department(
    dept_id: str,
    payload: DepartmentCreate,
    db: Session = Depends(get_db)
):
    return DepartmentService.update_department(
        dept_id,
        payload,
        db
    )


@router.delete("/{dept_id}")
def delete_department(
    dept_id: str,
    db: Session = Depends(get_db)
):
    return DepartmentService.delete_department(dept_id, db)