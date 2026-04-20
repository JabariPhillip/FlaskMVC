from sqlalchemy.orm import Session
from sqlmodel import select
from app.models.todo import Todo


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_todos(self, user_id: int) -> list[Todo]:
        statement = select(Todo).where(Todo.user_id == user_id)
        return self.db.exec(statement).all()