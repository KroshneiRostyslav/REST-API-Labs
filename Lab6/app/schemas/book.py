from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"


class BookBase(BaseModel):
    name: str
    author: str
    description: str
    year: int
    status: BookStatus


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: str
    created_at: datetime


class BookPage(BaseModel):
    items: list[BookResponse]
    total: int
    limit: int
    offset: int