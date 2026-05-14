from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import asyncio

from models.user import User
from utils.security import hash_password
from services.cache_service import CacheService


class UserService:

    @staticmethod
    def create_user(payload, db: Session):

        existing_email = (
            db.query(User)
            .filter(User.email == payload.email)
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        existing_phone = (
            db.query(User)
            .filter(User.phone == payload.phone)
            .first()
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already exists"
            )

        try:

            user = User(
                first_name=payload.first_name,
                last_name=payload.last_name,
                email=payload.email,
                password=hash_password(payload.password),
                phone=payload.phone
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            # Invalidate cache for all users
            asyncio.create_task(CacheService.invalidate_user_cache())

            return user

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry found"
            )

    @staticmethod
    async def get_all_users(cache_type: str, db: Session):
        if cache_type == "hot":
            cached_users = await CacheService.get_cached_all_users()
            if cached_users:
                return cached_users

        users = db.query(User).all()

        # Convert to dict for caching
        users_data = [
            {
                "user_id": str(user.user_id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone
            }
            for user in users
        ]

        # Cache the result (always cache after DB fetch)
        await CacheService.set_cached_all_users(users_data)

        return users_data

    @staticmethod
    async def get_user_by_id(user_id, db: Session):

        # Try to get from cache first
        cached_user = await CacheService.get_cached_user(user_id)
        if cached_user:
            return cached_user

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

        # Convert to dict for caching
        user_data = {
            "user_id": str(user.user_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone
        }

        # Cache the result
        await CacheService.set_cached_user(user_id, user_data)

        return user_data

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

        existing_email = (
            db.query(User)
            .filter(
                User.email == payload.email,
                User.user_id != user_id
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        existing_phone = (
            db.query(User)
            .filter(
                User.phone == payload.phone,
                User.user_id != user_id
            )
            .first()
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already exists"
            )

        try:

            user.first_name = payload.first_name
            user.last_name = payload.last_name
            user.email = payload.email
            user.password = hash_password(payload.password)
            user.phone = payload.phone

            db.commit()
            db.refresh(user)

            # Invalidate cache for this user and all users
            asyncio.create_task(CacheService.invalidate_user_cache(user_id))

            return user

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry found"
            )

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

        # Invalidate cache for this user and all users
        asyncio.create_task(CacheService.invalidate_user_cache(user_id))

        return {
            "message": "User deleted successfully"
        }