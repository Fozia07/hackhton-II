from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from ..models.user import User
from ..core.database import get_session
from .auth import get_current_user  # Using the existing auth function

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[TodoRead])
def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all todos for the current user.
    """
    statement = select(Todo).where(Todo.user_id == current_user.id)
    todos = session.exec(statement).all()
    return todos


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the current user.
    """
    todo = Todo(
        title=todo_create.title,
        description=todo_create.description,
        completed=todo_create.completed if hasattr(todo_create, 'completed') else False,
        user_id=current_user.id
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing todo.
    """
    # Get the existing todo
    todo = session.get(Todo, todo_id)

    # Check if todo exists and belongs to current user
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"  # Not revealing that the todo exists but belongs to another user
        )

    # Update the todo with provided fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a todo.
    """
    # Get the existing todo
    todo = session.get(Todo, todo_id)

    # Check if todo exists and belongs to current user
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"  # Not revealing that the todo exists but belongs to another user
        )

    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}