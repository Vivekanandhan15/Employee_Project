from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.auth_schema import (
    LoginSchema,
    TokenResponse
)
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: LoginSchema,
    db: Session = Depends(get_db)
):
    return AuthService.login(payload, db)

