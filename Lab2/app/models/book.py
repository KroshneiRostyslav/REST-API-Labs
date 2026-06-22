from uuid import UUID, uuid4
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