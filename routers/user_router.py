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
async def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Public endpoint to register a new user (no authentication required)."""
    return await UserService.create_user(payload, db)




@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    cache_type: str = "hot",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserService.get_all_users(cache_type, db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    cache_type: str = "cold",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserService.get_user_by_id(user_id, cache_type, db)


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserService.update_user(
        user_id,
        payload,
        db
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserService.delete_user(user_id, db)

