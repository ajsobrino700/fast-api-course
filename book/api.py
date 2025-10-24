from pydantic import BaseModel, Field
from typing import Optional


class BookAPI(BaseModel):
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


class Books(BaseModel):
    books: list[BookAPI]

    def __init__(self, books):
        super().__init__(books=[BookAPI(**book.__dict__) for book in books])
