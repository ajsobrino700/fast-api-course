from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


class Books(BaseModel):
    books: list[Book]


BOOKS = [
    Book(
        id=1,
        title="The selfish gene",
        author="Richard Dawkins",
        description="Holy shit",
        rating=7,
    ),
    Book(
        id=2,
        title="Fast API",
        author="Colombian Guy",
        description="Good framework",
        rating=5,
    ),
    Book(
        id=3,
        title="Introduction to Algorithms",
        author="Four guys",
        description="The best book, it is the bible",
        rating=11,
    ),
    Book(
        id=4,
        title="Crafting Interpreters",
        author="Robert Nystrom",
        description="A little practical introduction to interpreters",
        rating=8,
    ),
]


@app.get("/books")
async def get_all_books() -> Books:
    return Books(books=BOOKS)


@app.post("/book", status_code=201)
async def create_book(book: Book):
    BOOKS.append(book)
