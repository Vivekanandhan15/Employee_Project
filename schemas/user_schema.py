from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str

    class Config:
        from_attributes = True