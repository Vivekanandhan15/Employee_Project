from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from models.user import User
from utils.security import hash_password
from services.cache_service import CacheService


logger = logging.getLogger(__name__)


class UserService:

    @staticmethod
    def serialize_user(user: User):
        return {
            "user_id": str(user.user_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone
        }

    # =========================================================
    # CREATE USER
    # =========================================================
    @staticmethod
    async def create_user(payload, db: Session):

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

            # Invalidate Redis cache only
            await CacheService.invalidate_user_cache()

            logger.info("User created and cache invalidated")

            return UserService.serialize_user(user)

        except IntegrityError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry found"
            )

    # =========================================================
    # GET ALL USERS
    # =========================================================
    @staticmethod
    async def get_all_users(cache_type: str, db: Session):

        # HOT PATH -> REDIS ONLY
        if cache_type == "hot":

            cached_users = await CacheService.get_cached_all_users()

            if cached_users:
                logger.info("CACHE HIT -> ALL USERS")
                return cached_users

            logger.info("CACHE MISS -> ALL USERS")

            return []

        # COLD PATH -> POSTGRES ONLY
        users = db.query(User).all()

        logger.info("FETCHED ALL USERS FROM POSTGRES")

        users_data = [
            UserService.serialize_user(user)
            for user in users
        ]

        return users_data

    # =========================================================
    # GET USER BY ID
    # =========================================================
    @staticmethod
    async def get_user_by_id(user_id, cache_type: str, db: Session):

        # HOT PATH -> REDIS ONLY
        if cache_type == "hot":

            cached_user = await CacheService.get_cached_user(user_id)

            if cached_user:
                logger.info(f"CACHE HIT -> USER {user_id}")
                return cached_user

            logger.info(f"CACHE MISS -> USER {user_id}")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hot cache available"
            )

        # COLD PATH -> POSTGRES ONLY
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

        logger.info(f"FETCHED USER {user_id} FROM POSTGRES")

        return UserService.serialize_user(user)

    # =========================================================
    # UPDATE USER
    # =========================================================
    @staticmethod
    async def update_user(user_id, payload, db: Session):

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

            # Invalidate Redis cache only
            await CacheService.invalidate_user_cache(user_id)

            logger.info(f"User {user_id} updated and cache invalidated")

            return UserService.serialize_user(user)

        except IntegrityError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry found"
            )

    # =========================================================
    # DELETE USER
    # =========================================================
    @staticmethod
    async def delete_user(user_id, db: Session):

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

        # Invalidate Redis cache only
        await CacheService.invalidate_user_cache(user_id)

        logger.info(f"User {user_id} deleted and cache invalidated")

        return {
            "message": "User deleted successfully"
        }