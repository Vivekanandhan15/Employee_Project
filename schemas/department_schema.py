from uuid import UUID
from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    dept_name: str


class DepartmentResponse(BaseModel):
    dept_id: UUID
    dept_name: str

    class Config:
        from_attributes = True