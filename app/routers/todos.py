from fastapi import Request
from . import api_router
from app.dependencies import SessionDep
from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoResponse
from app.auth import AuthDep


@api_router.get("/todos", response_model=list[TodoResponse])
async def list_todos(request: Request, db: SessionDep, user: AuthDep):
    todo_repo = TodoRepository(db)
    return todo_repo.get_user_todos(user.id)
