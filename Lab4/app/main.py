from fastapi import FastAPI
from app.api.books import book_router

app = FastAPI()

app.include_router(book_router)

@app.get("/")
def root():
    return {"Для перегляду всіх книг скористатись /books префіксом"}