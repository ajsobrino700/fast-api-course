from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db

from auth.api import UserApi
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter()

bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, "secretKey")
        user_id: str = payload.get("id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unathorized"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not valid"
        )


@router.get("")
async def get_user():
    return {"user": "authenticated"}


@router.post("")
async def create_user(db: db_dependency, user_request: UserApi):
    user = User(
        username=user_request.username,
        email=user_request.email,
        role=user_request.role,
        hashed_password=bcrypt_context.hash(user_request.password),
    )

    db.add(user)
    db.commit()

    return {"id": user.id}


def create_access_token(
    username: str, role: str, user_id: int, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, "secretKey")


@router.post("/token")
async def get_token(
    db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {
        "access_token": create_access_token(
            user.username, user.role, user.id, timedelta(minutes=45)
        )
    }
