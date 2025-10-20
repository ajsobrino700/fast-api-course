from fastapi import FastAPI
from pydantic import BaseModel


class Book(BaseModel):
    tittle: str
    author: str
    category: str


app = FastAPI()


BOOKS: [Book] = [
    {
        "title": "Crafting Interpreters",
        "author": "Robert Nystrom",
        "category": "programming",
    },
    {
        "title": "Optimization Algorithms",
        "author": "Alaa Khamis",
        "category": "algorithms",
    },
    {
        "title": "The selfish gene",
        "author": "Richard Dawkins",
        "category": "science",
    },
]


@app.get("/api-endpoint")
async def first_api():
    return {"message": "Hello Antonio!"}


@app.get("/mybook")
async def favourite_book():
    return {"title": "Introduction to Algorithms"}


@app.get("/books")
async def read_all_books():
    return {"books": BOOKS}


@app.get("/books/category/{category}")
async def read_book_by_category(category: str):
    return {"books": list(filter(lambda x: x.get("category") == category, BOOKS))}


@app.get("/book")
async def books(category: str | None):
    return {"books": list(filter(lambda x: x.get("category") == category, BOOKS))}


@app.get("/book/author")
async def books_by_author(author: str):
    return {"books": list(filter(lambda x: x.get("author") == author, BOOKS))}


@app.post("/book", status_code=201)
async def create_book(book: Book):
    BOOKS.append(book)
    return
