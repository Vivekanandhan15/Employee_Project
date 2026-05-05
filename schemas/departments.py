from pydantic import BaseModel

class Department(BaseModel):
    dept_name:str

class DepartmentUpdate(Department):
    pass

