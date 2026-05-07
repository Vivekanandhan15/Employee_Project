from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.address_schema import (
    AddressCreate,
    AddressUpdate
)

from services.address_service import AddressService


router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)


@router.post("/users/{user_id}")
def create_address(
    user_id: UUID,
    payload: AddressCreate,
    db: Session = Depends(get_db)
):
    return AddressService.create_address(
        user_id,
        payload,
        db
    )


@router.get("/users/{user_id}")
def get_user_addresses(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    return AddressService.get_user_addresses(
        user_id,
        db
    )


@router.put("/{address_id}")
def update_address(
    address_id: UUID,
    payload: AddressUpdate,
    db: Session = Depends(get_db)
):
    return AddressService.update_address(
        address_id,
        payload,
        db
    )


@router.delete("/{address_id}")
def delete_address(
    address_id: UUID,
    db: Session = Depends(get_db)
):
    return AddressService.delete_address(
        address_id,
        db
    )