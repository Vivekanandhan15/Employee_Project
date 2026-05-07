from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name:str
    phone:str
    email: EmailStr
    password:str


class UserResponse(BaseModel):
    user_id: str
    first_name: str
    email: EmailStr

    class Config:
        from_attributes = True