from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from todo.models import Todo
from todo.database import get_db

router = APIRouter()


@router.get("")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todo).all()
