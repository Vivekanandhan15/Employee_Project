from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import asyncio

from models.user import User
from models.department import Department
from services.cache_service import CacheService


class UserDepartmentService:

    @staticmethod
    async def assign_users_departments(payload, db: Session):

        users = (
            db.query(User)
            .filter(User.user_id.in_(payload.user_ids))
            .all()
        )

        departments = (
            db.query(Department)
            .filter(Department.dept_id.in_(payload.department_ids))
            .all()
        )

        if not users:
            missing_user_ids = ", ".join(str(uid) for uid in payload.user_ids)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Users not found: {missing_user_ids}"
            )

        if not departments:
            missing_department_ids = ", ".join(str(uid) for uid in payload.department_ids)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Departments not found: {missing_department_ids}"
            )

        found_user_ids = {user.user_id for user in users}
        missing_user_ids = [str(uid) for uid in payload.user_ids if uid not in found_user_ids]
        if missing_user_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Users not found: {', '.join(missing_user_ids)}"
            )

        found_department_ids = {department.dept_id for department in departments}
        missing_department_ids = [str(uid) for uid in payload.department_ids if uid not in found_department_ids]
        if missing_department_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Departments not found: {', '.join(missing_department_ids)}"
            )

        for user in users:
            for department in departments:

                if department not in user.departments:
                    user.departments.append(department)

        db.commit()

        # Invalidate cache for affected users and departments
        for user in users:
            await CacheService.invalidate_user_department_cache(str(user.user_id))
        for department in departments:
            await CacheService.invalidate_user_department_cache(None, str(department.dept_id))

        return {
            "message": "Users assigned to departments successfully"
        }

    @staticmethod
    async def get_user_departments(user_id, db: Session):

        # Try to get from cache first
        cached_data = await CacheService.get_cached_user_departments(user_id)
        if cached_data:
            return cached_data

        # If not in cache, get from DB
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Cache the result (convert UUIDs to strings for JSON serialization)
        data = {
            "user_id": str(user.user_id),
            "name": f"{user.first_name} {user.last_name}",
            "departments": [
                {
                    "dept_id": str(department.dept_id),
                    "dept_name": department.dept_name
                }
                for department in user.departments
            ]
        }

        await CacheService.set_cached_user_departments(user_id, data)

        return data

    @staticmethod
    async def remove_user_from_department(user_id, dept_id, db: Session):

        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

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

        if department not in user.departments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not assigned to this department"
            )

        user.departments.remove(department)

        db.commit()

        # Invalidate cache for this user and department
        await CacheService.invalidate_user_department_cache(user_id, dept_id)

        return {
            "message": "User removed from department successfully"
        }

    @staticmethod
    async def get_department_users(dept_id, db: Session):

        # Try to get from cache first
        cached_data = await CacheService.get_cached_department_users(dept_id)
        if cached_data:
            return cached_data

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

        # Cache the result (stringify UUIDs so JSON serialization succeeds)
        data = {
            "dept_id": str(department.dept_id),
            "dept_name": department.dept_name,
            "users": [
                {
                    "user_id": str(user.user_id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone
                }
                for user in department.users
            ]
        }

        await CacheService.set_cached_department_users(dept_id, data)

        return data