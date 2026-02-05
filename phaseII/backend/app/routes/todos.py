from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from ..models.user import User
from ..core.database import get_session
from .auth import get_current_user  # Using the existing auth function

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[TodoRead])
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get all todos for the current user.
    """
    statement = select(Todo).where(Todo.user_id == current_user.id)
    result = await session.exec(statement)
    todos = result.all()
    return todos


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new todo for the current user.
    """
    current_time = datetime.utcnow()
    todo = Todo(
        title=todo_create.title,
        description=todo_create.description,
        completed=todo_create.completed if hasattr(todo_create, 'completed') else False,
        user_id=current_user.id,
        created_at=current_time,
        updated_at=current_time
    )
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update an existing todo.
    """
    # Get the existing todo
    todo = await session.get(Todo, todo_id)

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

    # Update the timestamp
    todo.updated_at = datetime.utcnow()

    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    return todo


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a todo.
    """
    # Get the existing todo
    todo = await session.get(Todo, todo_id)

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

    await session.delete(todo)
    await session.commit()
    return {"message": "Todo deleted successfully"}