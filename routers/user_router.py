from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth_dependency import get_current_user
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Public endpoint to register a new user (no authentication required)."""
    return UserService.create_user(payload, db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Protected endpoint to create user (requires authentication)."""
    return UserService.create_user(payload, db)


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserService.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserService.get_user_by_id(user_id, db)


@router.put("/{user_id}")
def update_user(
    user_id: str,
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserService.update_user(
        user_id,
        payload,
        db
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserService.delete_user(user_id, db)