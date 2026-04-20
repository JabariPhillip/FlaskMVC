from sqlmodel import SQLModel, Field
from typing import Optional


class TodoBase(SQLModel):
    title: str
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")


class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)