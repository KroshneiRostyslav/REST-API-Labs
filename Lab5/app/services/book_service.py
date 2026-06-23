from uuid import uuid4
from datetime import datetime

from app.repository.book_repository import BookRepository

class BookService:

    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def get_all_books(
        self,
        limit: int,
        offset: int
    ):
        books, total = await self.repository.get_all_books(
            limit,
            offset
        )

        return {
            "items": books,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    async def add_book(self, book_data):
        book = {
            "id": str(uuid4()),
            **book_data.model_dump(),
            "created_at": datetime.utcnow()
        }

        return await self.repository.add_book(book)

    async def get_book_by_id(
        self,
        book_id: str
    ):
        return await self.repository.get_book_by_id(
            book_id
        )

    async def delete_book_by_id(
        self,
        book_id: str
    ):
        return await self.repository.delete_book_by_id(
            book_id
        )