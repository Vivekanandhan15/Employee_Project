from uuid import UUID
from typing import List
from pydantic import BaseModel


class AssignDepartmentSchema(BaseModel):
    user_ids: List[UUID]
    department_ids: List[UUID]