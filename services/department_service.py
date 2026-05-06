from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.department import Department


class DepartmentService:

    @staticmethod
    def create_department(payload, db: Session):

        existing_department = (
            db.query(Department)
            .filter(Department.dept_name == payload.dept_name)
            .first()
        )

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department already exists"
            )

        department = Department(
            dept_name=payload.dept_name
        )

        db.add(department)
        db.commit()
        db.refresh(department)

        return department

    @staticmethod
    def get_all_departments(db: Session):
        return db.query(Department).all()

    @staticmethod
    def get_department_by_id(dept_id, db: Session):

        department = (
            db.query(Department)
            .filter(Department.dept_id == dept_id)
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        return department

    @staticmethod
    def update_department(dept_id, payload, db: Session):

        department = (
            db.query(Department)
            .filter(Department.dept_id == dept_id)
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        existing_department = (
            db.query(Department)
            .filter(
                Department.dept_name == payload.dept_name,
                Department.dept_id != dept_id
            )
            .first()
        )

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department name already exists"
            )

        department.dept_name = payload.dept_name

        db.commit()
        db.refresh(department)

        return department

    @staticmethod
    def delete_department(dept_id, db: Session):

        department = (
            db.query(Department)
            .filter(Department.dept_id == dept_id)
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        db.delete(department)
        db.commit()

        return {
            "message": "Department deleted successfully"
        }