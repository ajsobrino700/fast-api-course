from fastapi import FastAPI
from database import engine, SessionLocal
from todo.router import router as todo_router
from book.router import router as book_router
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(router=todo_router, prefix="/todo", tags=["Todo"])
app.include_router(router=book_router, prefix="/book", tags=["Book"])
