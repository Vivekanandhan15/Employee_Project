from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user import User
from models.department import Department


class UserDepartmentService:

    @staticmethod
    def assign_users_departments(payload, db: Session):

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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found"
            )

        if not departments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Departments not found"
            )

        for user in users:
            for department in departments:

                if department not in user.departments:
                    user.departments.append(department)

        db.commit()

        return {
            "message": "Users assigned to departments successfully"
        }

    @staticmethod
    def get_user_departments(user_id, db: Session):

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

        return {
            "user_id": user.user_id,
            "name": user.name,
            "departments": user.departments
        }

    @staticmethod
    def remove_user_from_department(user_id, dept_id, db: Session):

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

        return {
            "message": "User removed from department successfully"
        }

    @staticmethod
    def get_department_users(dept_id, db: Session):

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

        return {
            "dept_id": department.dept_id,
            "dept_name": department.dept_name,
            "users": department.users
        }