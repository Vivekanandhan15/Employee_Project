from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    dept_name: str


class DepartmentResponse(BaseModel):
    dept_id: str
    dept_name: str

    class Config:
        from_attributes = True