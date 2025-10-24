from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from todo.api import TodoApi
from models import Todo
from database import get_db
from starlette import status
from auth.router import get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("")
async def read_all(user: user_dependency, db: Annotated[Session, Depends(get_db)]):
    return db.query(Todo).filter(Todo.owner_id == user).all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, id: int = Path(ge=0)):
    todo_model = (
        db.query(Todo).filter(Todo.id == id).filter(Todo.owner_id == user).first()
    )
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not exist")
    return todo_model


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo: TodoApi):
    todo_model = Todo(**todo.model_dump(), owner_id=user)
    db.add(todo_model)
    db.commit()
    return {"id": todo_model.id}


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency, db: db_dependency, todo: TodoApi, todo_id: int = Path(gt=0)
):
    todo_saved = (
        db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user).first()
    )
    if not todo_saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todo_saved.title = todo.title
    todo_saved.description = todo.description
    todo_saved.complete = todo.complete
    todo_saved.priority = todo.priority
    db.add(todo_saved)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    todo_saved = (
        db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user).first()
    )
    if not todo_saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo_saved)
    db.commit()
