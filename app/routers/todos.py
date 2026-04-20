from fastapi import APIRouter, Request, Form, status
from app.dependencies import SessionDep
from sqlmodel import select
from app.models.todos import Todo
from app.auth import AuthDep
from fastapi.responses import HTMLResponse, RedirectResponse
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

@todo_router.post("/todos")
async def create_todo(
    request: Request,
    title: str = Form(...),
    user: AuthDep = None,
    db: SessionDep = None
):
    new_todo = Todo(
        title=title,
        completed=False,
        user_id=user.id
    )

    db.add(new_todo)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

@todo_router.post("/todos/{todo_id}/toggle")
async def toggle_todo(
    todo_id: int,
    request: Request,
    user: AuthDep,
    db: SessionDep
):
    todo = db.exec(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    ).one_or_none()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = not todo.completed
    db.add(todo)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)


@todo_router.post("/todos/{todo_id}/delete")
async def delete_todo(
    todo_id: int,
    request: Request,
    user: AuthDep,
    db: SessionDep
):
    todo = db.exec(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    ).one_or_none()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)