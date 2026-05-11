from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import asyncio

from models.department import Department
from services.cache_service import CacheService


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

        # Invalidate cache for all departments
        asyncio.create_task(CacheService.invalidate_department_cache())

        return department

    @staticmethod
    async def get_all_departments(db: Session):
        # Try to get from cache first
        cached_departments = await CacheService.get_cached_all_departments()
        if cached_departments:
            return cached_departments

        # If not in cache, get from DB
        departments = db.query(Department).all()

        # Convert to dict for caching
        departments_data = [
            {
                "dept_id": str(department.dept_id),
                "dept_name": department.dept_name
            }
            for department in departments
        ]

        # Cache the result
        await CacheService.set_cached_all_departments(departments_data)

        return departments_data

    @staticmethod
    async def get_department_by_id(dept_id, db: Session):

        # Try to get from cache first
        cached_department = await CacheService.get_cached_department(dept_id)
        if cached_department:
            return cached_department

        # If not in cache, get from DB
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

        # Convert to dict for caching
        department_data = {
            "dept_id": str(department.dept_id),
            "dept_name": department.dept_name
        }

        # Cache the result
        await CacheService.set_cached_department(dept_id, department_data)

        return department_data

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

        # Invalidate cache for this department and all departments
        asyncio.create_task(CacheService.invalidate_department_cache(dept_id))

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

        # Invalidate cache for this department and all departments
        asyncio.create_task(CacheService.invalidate_department_cache(dept_id))

        return {
            "message": "Department deleted successfully"
        }