from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user import User
from utils.security import verify_password
from utils.jwt_handler import create_access_token


class AuthService:

    @staticmethod
    def login(payload, db: Session):

        user = (
            db.query(User)
            .filter(User.email == payload.email)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(
            payload.password,
            user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token(
            data={
                "sub": str(user.user_id),
                "email": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }