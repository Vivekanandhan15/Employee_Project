from uuid import UUID
from pydantic import BaseModel


class AddressCreate(BaseModel):
    address_line_1: str
    address_line_2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str


class AddressUpdate(BaseModel):
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


class AddressResponse(BaseModel):
    address_id: UUID

    address_line_1: str
    address_line_2: str | None = None

    city: str
    state: str
    country: str
    postal_code: str

    user_id: UUID

    class Config:
        from_attributes = True