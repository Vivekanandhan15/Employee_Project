import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base


class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255))

    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)

    country = Column(String(100), nullable=False)

    postal_code = Column(String(20), nullable=False)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="addresses"
    )