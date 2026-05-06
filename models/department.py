import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base
from models.association import user_department


class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    dept_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    users = relationship(
        "User",
        secondary=user_department,
        back_populates="departments"
    )