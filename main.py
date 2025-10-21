from fastapi import FastAPI
from todo.router import router as todo_router
from book.router import router as book_router

app = FastAPI()

app.include_router(router=todo_router, prefix="/todo", tags=["Todo"])
app.include_router(router=book_router, prefix="/book", tags=["Book"])
