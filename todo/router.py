from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from todo.api import TodoApi
from todo.models import Todo
from todo.database import get_db
from starlette import status

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todo).all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, id: int = Path(ge=0)):
    todo_model = db.query(Todo).filter(Todo.id == id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not exist")
    return todo_model


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo: TodoApi):
    todo_model = Todo(**todo.model_dump())
    db.add(todo_model)
    db.commit()
    return {"id": todo_model.id}


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo: TodoApi, todo_id: int = Path(gt=0)):
    todo_saved = db.query(Todo).filter(Todo.id == todo_id).first()
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
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_saved = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo_saved)
    db.commit()
