from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"

class BookSort(str, Enum):
    by_name = "name"
    by_year = "year"

class BookBase(BaseModel):
    name: str   
    author: str
    description: str
    year: int
    status: BookStatus

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID