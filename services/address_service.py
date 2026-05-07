from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user import User
from models.address import Address

from schemas.address_schema import (
    AddressCreate,
    AddressUpdate
)


class AddressService:

    @staticmethod
    def create_address(
        user_id: UUID,
        payload: AddressCreate,
        db: Session
    ):

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

        address = Address(
            **payload.model_dump(),
            user_id=user_id
        )

        db.add(address)
        db.commit()
        db.refresh(address)

        return {
            "message": "Address created successfully",
            "data": address
        }

    @staticmethod
    def get_user_addresses(
        user_id: UUID,
        db: Session
    ):

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
            "message": "Addresses fetched successfully",
            "data": user.addresses
        }

    @staticmethod
    def update_address(
        address_id: UUID,
        payload: AddressUpdate,
        db: Session
    ):

        address = (
            db.query(Address)
            .filter(Address.address_id == address_id)
            .first()
        )

        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )

        update_data = payload.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(address, key, value)

        db.commit()
        db.refresh(address)

        return {
            "message": "Address updated successfully",
            "data": address
        }

    @staticmethod
    def delete_address(
        address_id: UUID,
        db: Session
    ):

        address = (
            db.query(Address)
            .filter(Address.address_id == address_id)
            .first()
        )

        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )

        db.delete(address)
        db.commit()

        return {
            "message": "Address deleted successfully"
        }