from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from database.database import Base

user_department = Table(
    "user_departments",
    Base.metadata,

    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "department_id",
        UUID(as_uuid=True),
        ForeignKey("departments.dept_id", ondelete="CASCADE"),
        primary_key=True
    )
)