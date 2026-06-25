from app.database import db


class BookRepository:

    def __init__(self):
        self.collection = db.books

    def get_all_books(
        self,
        limit,
        offset
    ):
        books = list(
            self.collection
            .find({})
            .skip(offset)
            .limit(limit)
        )

        for book in books:
            book.pop("_id", None)

        total = self.collection.count_documents({})

        return books, total

    def get_book_by_id(
        self,
        book_id
    ):
        book = self.collection.find_one(
            {"id": book_id}
        )

        if book:
            book.pop("_id", None)

        return book

    def add_book(
        self,
        data
    ):
        self.collection.insert_one(data)

        data.pop("_id", None)

        return data

    def delete_book_by_id(
        self,
        book_id
    ):
        result = self.collection.delete_one(
            {"id": book_id}
        )

        return result.deleted_count > 0