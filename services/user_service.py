from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user import User


class UserService:

    @staticmethod
    def create_user(payload, db: Session):

        existing_user = (
            db.query(User)
            .filter(User.email == payload.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email = payload.email,
            password = payload.password,
            phone = payload.phone
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(user_id, db: Session):

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

        return user

    @staticmethod
    def update_user(user_id, payload, db: Session):

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

        existing_user = (
            db.query(User)
            .filter(
                User.email == payload.email,
                User.user_id != user_id
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        user.first_name = payload.first_name
        user.last_name = payload.last_name
        user.email = payload.email
        user.password = payload.password
        user.phone=payload.phone


        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(user_id, db: Session):

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

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }