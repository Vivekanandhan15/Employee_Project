import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base
from models.association import user_department


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password = Column(String, nullable=False)

    phone = Column(
        String(15),
        unique=True,
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # MANY TO MANY
    departments = relationship(
        "Department",
        secondary=user_department,
        back_populates="users"
    )

    # ONE TO MANY
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan"
    )