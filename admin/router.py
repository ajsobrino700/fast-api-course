from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Annotated
from starlette import status
from database import get_db
from models import User
from auth.router import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin", tags=["admin"])

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user)
    db.commit()
