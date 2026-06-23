from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str]
    author: Mapped[str]
    description: Mapped[str]
    year: Mapped[int]
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )