# API Contract: Task Management Endpoints

**Feature**: 001-todo-frontend | **Date**: 2026-01-07 | **Version**: 1.0

## Purpose

Define the task management API contract between the Next.js frontend and FastAPI backend. This contract ensures both teams can develop independently while maintaining compatibility.

## Base URL

```
Production: https://api.example.com
Development: http://localhost:8000
```

## Authentication

All task endpoints require JWT authentication via the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## User Isolation

All task operations are scoped to the authenticated user. Users can only access their own tasks. The backend enforces user isolation based on the JWT token's `sub` claim (user ID).

## Endpoints

### GET /api/v1/tasks

Get all tasks for the authenticated user.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**: None (filtering done client-side)

**Success Response** (200 OK):
```json
{
  "data": [
    {
      "id": "tsk_1234567890",
      "title": "Buy groceries",
      "completed": false,
      "userId": "usr_1234567890",
      "createdAt": "2026-01-07T12:00:00Z",
      "updatedAt": "2026-01-07T12:00:00Z"
    },
    {
      "id": "tsk_0987654321",
      "title": "Finish project",
      "completed": true,
      "userId": "usr_1234567890",
      "createdAt": "2026-01-06T10:00:00Z",
      "updatedAt": "2026-01-07T11:00:00Z"
    }
  ]
}
```

**Empty Response** (200 OK):
```json
{
  "data": []
}
```

**Error Responses**:

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### POST /api/v1/tasks

Create a new task for the authenticated user.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries"
}
```

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 500 characters

**Success Response** (201 Created):
```json
{
  "data": {
    "id": "tsk_1234567890",
    "title": "Buy groceries",
    "completed": false,
    "userId": "usr_1234567890",
    "createdAt": "2026-01-07T12:00:00Z",
    "updatedAt": "2026-01-07T12:00:00Z"
  },
  "message": "Task created successfully"
}
```

**Error Responses**:

400 Bad Request - Validation Error:
```json
{
  "message": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "title": ["Task title is required"]
  }
}
```

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### GET /api/v1/tasks/{id}

Get a specific task by ID (must belong to authenticated user).

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
- `id`: Task ID (e.g., `tsk_1234567890`)

**Success Response** (200 OK):
```json
{
  "data": {
    "id": "tsk_1234567890",
    "title": "Buy groceries",
    "completed": false,
    "userId": "usr_1234567890",
    "createdAt": "2026-01-07T12:00:00Z",
    "updatedAt": "2026-01-07T12:00:00Z"
  }
}
```

**Error Responses**:

404 Not Found - Task Not Found or Not Owned:
```json
{
  "message": "Task not found",
  "code": "TASK_NOT_FOUND"
}
```

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### PUT /api/v1/tasks/{id}

Update a task (full update, must belong to authenticated user).

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters**:
- `id`: Task ID (e.g., `tsk_1234567890`)

**Request Body**:
```json
{
  "title": "Buy groceries and cook dinner",
  "completed": true
}
```

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 500 characters
- `completed`: Required, boolean

**Success Response** (200 OK):
```json
{
  "data": {
    "id": "tsk_1234567890",
    "title": "Buy groceries and cook dinner",
    "completed": true,
    "userId": "usr_1234567890",
    "createdAt": "2026-01-07T12:00:00Z",
    "updatedAt": "2026-01-07T13:00:00Z"
  },
  "message": "Task updated successfully"
}
```

**Error Responses**:

400 Bad Request - Validation Error:
```json
{
  "message": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "title": ["Task title must be less than 500 characters"]
  }
}
```

404 Not Found - Task Not Found or Not Owned:
```json
{
  "message": "Task not found",
  "code": "TASK_NOT_FOUND"
}
```

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### PATCH /api/v1/tasks/{id}

Partially update a task (must belong to authenticated user).

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters**:
- `id`: Task ID (e.g., `tsk_1234567890`)

**Request Body** (all fields optional):
```json
{
  "completed": true
}
```

**Validation Rules**:
- `title`: Optional, minimum 1 character, maximum 500 characters
- `completed`: Optional, boolean

**Success Response** (200 OK):
```json
{
  "data": {
    "id": "tsk_1234567890",
    "title": "Buy groceries",
    "completed": true,
    "userId": "usr_1234567890",
    "createdAt": "2026-01-07T12:00:00Z",
    "updatedAt": "2026-01-07T13:00:00Z"
  },
  "message": "Task updated successfully"
}
```

**Error Responses**:

400 Bad Request - Validation Error:
```json
{
  "message": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "completed": ["Must be a boolean value"]
  }
}
```

404 Not Found - Task Not Found or Not Owned:
```json
{
  "message": "Task not found",
  "code": "TASK_NOT_FOUND"
}
```

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### DELETE /api/v1/tasks/{id}

Delete a task (must belong to authenticated user).

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
- `id`: Task ID (e.g., `tsk_1234567890`)

**Success Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:

404 Not Found - Task Not Found or Not Owned:
```json
{
  "message": "Task not found",
  "code": "TASK_NOT_FOUND"
}
```

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

## Data Model

### Task Object

```typescript
interface Task {
  id: string              // Unique task identifier (e.g., "tsk_1234567890")
  title: string           // Task title (1-500 characters)
  completed: boolean      // Completion status
  userId: string          // Owner user ID (e.g., "usr_1234567890")
  createdAt: string       // ISO 8601 timestamp
  updatedAt: string       // ISO 8601 timestamp
}
```

## Error Code Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Request validation failed |
| INVALID_TOKEN | 401 | JWT token invalid or expired |
| TASK_NOT_FOUND | 404 | Task not found or not owned by user |
| INTERNAL_ERROR | 500 | Unexpected server error |

## Rate Limiting

- GET /api/v1/tasks: 60 requests per minute per user
- POST /api/v1/tasks: 30 requests per minute per user
- GET /api/v1/tasks/{id}: 60 requests per minute per user
- PUT /api/v1/tasks/{id}: 30 requests per minute per user
- PATCH /api/v1/tasks/{id}: 30 requests per minute per user
- DELETE /api/v1/tasks/{id}: 30 requests per minute per user

## CORS Configuration

**Allowed Origins**:
- Production: `https://app.example.com`
- Development: `http://localhost:3000`

**Allowed Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS

**Allowed Headers**: Content-Type, Authorization

**Credentials**: true (for cookies)

## Testing Scenarios

### Happy Path

1. User creates task → 201 Created
2. User lists tasks → 200 OK with task in list
3. User marks task complete (PATCH) → 200 OK
4. User edits task title (PUT) → 200 OK
5. User deletes task → 200 OK
6. User lists tasks → 200 OK with empty list

### Error Scenarios

1. User creates task with empty title → 400 Bad Request
2. User tries to access another user's task → 404 Not Found
3. User makes request with expired JWT → 401 Unauthorized
4. User tries to update non-existent task → 404 Not Found
5. User creates task with title > 500 characters → 400 Bad Request

## Frontend Implementation Notes

### API Client Methods

```typescript
// lib/api/client.ts
export const api = {
  async get<T>(endpoint: string): Promise<T> {
    const token = await getJWTToken()
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    })
    if (!response.ok) throw new Error("Request failed")
    return response.json()
  },

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    const token = await getJWTToken()
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw new Error("Request failed")
    return response.json()
  },

  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    const token = await getJWTToken()
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      method: "PATCH",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw new Error("Request failed")
    return response.json()
  },

  async delete(endpoint: string): Promise<void> {
    const token = await getJWTToken()
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    })
    if (!response.ok) throw new Error("Request failed")
  },
}
```

### React Query Hooks

```typescript
// hooks/useTasks.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api/client"

export function useTasks() {
  return useQuery({
    queryKey: ["tasks"],
    queryFn: () => api.get<{ data: Task[] }>("/api/v1/tasks").then(res => res.data),
  })
}

export function useCreateTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { title: string }) =>
      api.post<{ data: Task }>("/api/v1/tasks", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })
}

export function useToggleTaskComplete(taskId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (completed: boolean) =>
      api.patch(`/api/v1/tasks/${taskId}`, { completed }),
    onMutate: async (completed) => {
      await queryClient.cancelQueries({ queryKey: ["tasks"] })
      const previousTasks = queryClient.getQueryData(["tasks"])
      queryClient.setQueryData(["tasks"], (old: Task[]) =>
        old.map(task => task.id === taskId ? { ...task, completed } : task)
      )
      return { previousTasks }
    },
    onError: (err, variables, context) => {
      queryClient.setQueryData(["tasks"], context.previousTasks)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })
}

export function useDeleteTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (taskId: string) => api.delete(`/api/v1/tasks/${taskId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })
}
```

## Backend Implementation Notes

### User Isolation Enforcement

```python
# backend/src/api/tasks.py
from fastapi import Depends, HTTPException
from src.auth.jwt import get_current_user

@router.get("/api/v1/tasks")
async def get_tasks(current_user: User = Depends(get_current_user)):
    # Only return tasks owned by current user
    tasks = await Task.filter(user_id=current_user.id).all()
    return {"data": tasks}

@router.get("/api/v1/tasks/{task_id}")
async def get_task(task_id: str, current_user: User = Depends(get_current_user)):
    task = await Task.get_or_none(id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"data": task}
```

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-07 | Initial contract definition |

## Approval

- Frontend Team: Pending
- Backend Team: Pending
- Security Review: Pending
