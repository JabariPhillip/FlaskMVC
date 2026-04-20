from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlmodel import select
from app.repositories.todos import TodoRepository
from app.schemas.todo import TodoResponse
from app.database import SessionDep
from app.models import *
from app.auth import AuthDep
from . import templates

app_router = APIRouter()


@app_router.get("/app", response_class=HTMLResponse)
async def app(
    request: Request,
    user: AuthDep,
    db: SessionDep
):
    return templates.TemplateResponse(
        request=request, 
        name="app.html",
        context={
            "user": user
        }
    )


@app_router.get("/todos", response_class=HTMLResponse)
async def todos_page(
    request: Request,
    user: AuthDep,
    db: SessionDep
):
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