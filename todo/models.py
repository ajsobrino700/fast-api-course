from todo.database import Base
from sqlalchemy import Column, String, Integer, Boolean


class Todo(Base):

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, name="description_task")
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
