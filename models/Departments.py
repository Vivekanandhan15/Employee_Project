from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database.database import Base


class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dpet_name = Column(String(100), unique=True, nullable=False)
    users = relationship("User", back_populates="department")