from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        default=None, description="The internal identifier of the book"
    )
    title: str = Field(min_length=5)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=0, le=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithantonio",
                "description": "A new description",
                "rating": 10,
            }
        }
    }


class Books:
    books: list[Book]

    def __init__(self, books):
        self.books = books


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
async def get_all_books():
    return Books(books=BOOKS)


@app.get("/book/{id}")
async def get_book_by_id(id: int = Path(gt=0)):
    book = next(filter(lambda book: book.id == id, BOOKS), None)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@app.get("/books/")
async def get_by_rating(book_rating: int = Query(ge=0, le=10)):
    return list(filter(lambda book: book.rating == book_rating, BOOKS))


@app.put("/book/{id}")
async def update_book(book_request: BookRequest, id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            book_request.id = id
            BOOKS[i] = Book(**book_request.model_dump())
    return {"id": id}


@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int = Path(gt=0)):
    find = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            find = True

    if not find:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The book not exist"
        )


@app.post("/book", status_code=status.HTTP_204_NO_CONTENT)
async def create_book(book_request: BookRequest):
    BOOKS.append(Book(**book_request.model_dump()))
