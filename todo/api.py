from pydantic import BaseModel, Field


class TodoApi(BaseModel):

    title: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=1000)
    priority: int = Field(ge=0, le=5)
    complete: bool = Field(default=False)
