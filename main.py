from fastapi import FastAPI
from todo.router import router as todo_router
from book.router import router as book_router
from auth.router import router as auth_router
from admin.router import router as admin_router

app = FastAPI()

app.include_router(router=todo_router, prefix="/todo", tags=["Todo"])
app.include_router(router=book_router, prefix="/book", tags=["Book"])
app.include_router(router=auth_router, prefix="/auth", tags=["Auth"])
app.include_router(router=admin_router)


@app.get("/health")
def health_check():
    return {"status": "Health"}
