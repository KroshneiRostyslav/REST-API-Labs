from uuid import UUID

from app.models.books import books
from app.schemas.book import BookStatus, BookSort

class BookRepository:
    async def get_all_books(
        self,
        author: str | None = None,
        status: BookStatus | None = None,
        sort: BookSort | None = None
    ):
        result = books

        if author:
            result = [
                book
                for book in result
                if book["author"] == author
            ]
        
        if status: 
            result = [
                book
                for book in result
                if book["status"] == status.value
            ]

        if sort == BookSort.by_name:
            result = sorted(
                result,
                key=lambda book: book["name"]
            )

        if sort == BookSort.by_year:
            result = sorted(
                result,
                key=lambda book: book["year"]
            )

        return result

    async def get_book_by_id(self, book_id: UUID):
        for book in books:
            if book["id"] == str(book_id):
                return book
        
        return None
    
    async def add_book(self, book_dict: dict):
        books.append(book_dict)
        return book_dict
    
    async def delete_book_by_id(self, book_id: UUID):
        for index, book in enumerate(books):
            if book["id"] == str(book_id):
                books.pop(index)
                return True

        return False