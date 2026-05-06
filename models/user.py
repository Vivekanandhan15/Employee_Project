import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base
from models.association import user_department


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    departments = relationship(
        "Department",
        secondary=user_department,
        back_populates="users"
    )