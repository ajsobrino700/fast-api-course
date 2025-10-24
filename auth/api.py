from pydantic import BaseModel, Field


class UserApi(BaseModel):

    username: str
    email: str
    password: str
    role: str
