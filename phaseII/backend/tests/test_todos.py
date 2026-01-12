import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.main import app
from app.core.database import engine
from app.models.user import User
from app.models.todo import Todo
from app.core.security import get_password_hash


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    import time
    unique_id = str(int(time.time() * 1000))  # Use timestamp for uniqueness
    hashed_password = get_password_hash("testpassword123")
    user = User(
        username=f"testuser_{unique_id}",
        email=f"test_{unique_id}@example.com",
        hashed_password=hashed_password
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def test_create_todo(client, sample_user):
    """Test creating a new todo"""
    # First, authenticate to get a token
    response = client.post(
        "/auth/signin",
        json={
            "username": sample_user.username,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Now create a todo with the token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }

    response = client.post("/todos/", json=todo_data, headers=headers)
    assert response.status_code == 201

    created_todo = response.json()
    assert created_todo["title"] == "Test Todo"
    assert created_todo["description"] == "Test Description"
    assert created_todo["user_id"] == sample_user.id
    assert created_todo["completed"] is False


def test_get_todos(client, sample_user):
    """Test getting todos for a user"""
    # Authenticate first
    response = client.post(
        "/auth/signin",
        json={
            "username": sample_user.username,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Create a todo
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    todo_data = {
        "title": "Another Test Todo",
        "description": "Another Test Description"
    }

    response = client.post("/todos/", json=todo_data, headers=headers)
    assert response.status_code == 201

    # Get all todos
    response = client.get("/todos/", headers=headers)
    assert response.status_code == 200

    todos = response.json()
    assert len(todos) >= 1
    assert any(todo["title"] == "Another Test Todo" for todo in todos)


def test_update_todo(client, sample_user):
    """Test updating a todo"""
    # Authenticate first
    response = client.post(
        "/auth/signin",
        json={
            "username": sample_user.username,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Create a todo
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    todo_data = {
        "title": "Original Todo",
        "description": "Original Description"
    }

    response = client.post("/todos/", json=todo_data, headers=headers)
    assert response.status_code == 201
    created_todo = response.json()

    # Update the todo
    update_data = {
        "title": "Updated Todo",
        "completed": True
    }

    response = client.put(f"/todos/{created_todo['id']}", json=update_data, headers=headers)
    assert response.status_code == 200

    updated_todo = response.json()
    assert updated_todo["title"] == "Updated Todo"
    assert updated_todo["completed"] is True


def test_delete_todo(client, sample_user):
    """Test deleting a todo"""
    # Authenticate first
    response = client.post(
        "/auth/signin",
        json={
            "username": sample_user.username,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Create a todo
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    todo_data = {
        "title": "Todo to Delete",
        "description": "Description to Delete"
    }

    response = client.post("/todos/", json=todo_data, headers=headers)
    assert response.status_code == 201
    created_todo = response.json()

    # Delete the todo
    response = client.delete(f"/todos/{created_todo['id']}", headers=headers)
    assert response.status_code == 200

    # Verify the todo is deleted by trying to get it again
    response = client.get("/todos/", headers=headers)
    assert response.status_code == 200
    todos = response.json()
    assert not any(todo["id"] == created_todo["id"] for todo in todos)


if __name__ == "__main__":
    pytest.main()