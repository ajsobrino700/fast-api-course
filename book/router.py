from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status

from .models import Book, BOOKS
from .api import BookAPI, Books

router = APIRouter()


@router.get("")
async def get_all_books() -> Books:
    return Books(books=BOOKS)


@router.get("/{id}")
async def get_book_by_id(id: int = Path(gt=0)):
    book = next(filter(lambda book: book.id == id, BOOKS), None)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@router.get("/")
async def get_by_rating(book_rating: int = Query(ge=0, le=10)):
    return list(filter(lambda book: book.rating == book_rating, BOOKS))


@router.put("/{id}")
async def update_book(book_request: BookAPI, id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            book_request.id = id
            BOOKS[i] = Book(**book_request.model_dump())
    return {"id": id}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def create_book(book_request: BookAPI):
    BOOKS.append(Book(**book_request.model_dump()))
