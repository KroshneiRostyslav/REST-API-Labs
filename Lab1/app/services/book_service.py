from uuid import uuid4, UUID

from app.schemas.book import BookCreate, BookStatus, BookSort
from app.repository.book_repository import BookRepository

class BookServices:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def get_all_books(
        self,
        author: str | None = None,
        status: BookStatus | None = None,
        sort: BookSort | None = None
    ):
        return await self.repository.get_all_books(author, status, sort)

    async def get_book_by_id(self, book_id: UUID):
        return await self.repository.get_book_by_id(book_id)

    async def add_book(self, book:BookCreate):
        return await self.repository.add_book(
            {
                "id": str(uuid4()),
                **book.model_dump()
            }
        )
    
    async def delete_book_by_id(self, book_id: UUID):
        return await self.repository.delete_book_by_id(book_id)