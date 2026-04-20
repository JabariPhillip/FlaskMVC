from sqlmodel import SQLModel
from typing import Optional


class TodoCreate(SQLModel):
    title: str


class TodoResponse(SQLModel):
    id: int
    title: str
    completed: bool
    user_id: int