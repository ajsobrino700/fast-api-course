from sqlalchemy.orm.properties import ForeignKey
from database import Base
from sqlalchemy import Column, String, Integer, Boolean


class Todo(Base):

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, name="description_task")
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
