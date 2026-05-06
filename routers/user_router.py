from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.user_schema import UserCreate
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.create_user(payload, db)


@router.get("/")
def get_all_users(
    db: Session = Depends(get_db)
):
    return UserService.get_all_users(db)


@router.get("/{user_id}")
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db)
):
    return UserService.get_user_by_id(user_id, db)


@router.put("/{user_id}")
def update_user(
    user_id: str,
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.update_user(
        user_id,
        payload,
        db
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    return UserService.delete_user(user_id, db)