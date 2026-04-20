from fastapi import APIRouter, Request
from app.dependencies import SessionDep
from sqlmodel import select
from app.models.todos import Todo
from app.auth import AuthDep
from fastapi.responses import HTMLResponse
from . import templates

todo_router = APIRouter()


@todo_router.get("/todos", response_class=HTMLResponse)
async def todos_page(request: Request, user: AuthDep, db: SessionDep):
    todos = db.exec(
        select(Todo).where(Todo.user_id == user.id)
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={
            "user": user,
            "todos": todos
        }
    )
