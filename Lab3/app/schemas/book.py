from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from datetime import datetime
    
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
    id: str
    created_at: datetime

class BookPage(BaseModel):
    items: list[BookResponse]
    total: int
    limit: int
    offset: int