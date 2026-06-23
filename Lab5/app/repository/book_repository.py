class BookRepository:

    def __init__(self, db):
        self.collection = db.books

    async def get_all_books(
        self,
        limit: int,
        offset: int
    ):
        cursor = (
            self.collection
                .find()
                .sort("created_at", 1)
                .skip(offset)
                .limit(limit)
        )

        books = await cursor.to_list(length=limit)

        for book in books:
            book.pop("_id", None)

        total = await self.collection.count_documents({})

        return books, total

    async def get_book_by_id(self, book_id: str):
        book = await self.collection.find_one(
            {"id": book_id}
        )

        if book:
            book.pop("_id", None)

        return book

    async def add_book(
        self,
        data: dict
    ):
        await self.collection.insert_one(data)

        return data

    async def delete_book_by_id(
        self,
        book_id: str
    ):
        result = await self.collection.delete_one(
            {"id": book_id}
        )

        return result.deleted_count > 0