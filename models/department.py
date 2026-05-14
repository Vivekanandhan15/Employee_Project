import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

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

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    users = relationship(
        "User",
        secondary=user_department,
        back_populates="departments"
    )