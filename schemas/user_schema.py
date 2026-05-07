from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    first_name: str
    last_name:str
    phone:str
    email: EmailStr
    password:str


class UserResponse(BaseModel):
    user_id: UUID
    first_name: str
    email: EmailStr

    class Config:
        from_attributes = True