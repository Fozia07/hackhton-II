# Data Model: Todo Web Application Frontend

**Feature**: 001-todo-frontend | **Date**: 2026-01-07 | **Phase**: 1 (Design)

## Purpose

Define frontend data structures, state shape, and type definitions for the Todo Web Application. This document serves as the single source of truth for TypeScript types and data flow patterns.

## Core Data Types

### User

Represents an authenticated user in the application.

```typescript
// types/auth.ts

export interface User {
  id: string
  email: string
  name: string
  createdAt: string // ISO 8601 timestamp
}

export interface Session {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: Error | null
}

export interface AuthCredentials {
  email: string
  password: string
}

export interface SignupData extends AuthCredentials {
  name: string
}
```

**Usage**:
- `User`: Returned from authentication endpoints, stored in session
- `Session`: Managed by Better Auth, accessed via useAuth hook
- `AuthCredentials`: Login form data
- `SignupData`: Signup form data

**Validation Rules**:
- `email`: Must be valid email format (RFC 5322)
- `password`: Minimum 8 characters, at least one uppercase, one lowercase, one number
- `name`: Minimum 2 characters, maximum 100 characters

### Task

Represents a todo item owned by a user.

```typescript
// types/task.ts

export interface Task {
  id: string
  title: string
  completed: boolean
  userId: string
  createdAt: string // ISO 8601 timestamp
  updatedAt: string // ISO 8601 timestamp
}

export interface CreateTaskInput {
  title: string
}

export interface UpdateTaskInput {
  title?: string
  completed?: boolean
}

export type TaskFilter = "all" | "active" | "completed"

export interface TaskListState {
  tasks: Task[]
  filter: TaskFilter
  searchQuery: string
  isLoading: boolean
  error: Error | null
}
```

**Usage**:
- `Task`: Returned from task endpoints, displayed in task list
- `CreateTaskInput`: Create task form data
- `UpdateTaskInput`: Edit task form data (partial update)
- `TaskFilter`: Filter state for task list
- `TaskListState`: Complete task list component state

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 500 characters
- `completed`: Boolean, defaults to false

### API Response Types

Standard response wrappers for API calls.

```typescript
// types/api.ts

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface ApiError {
  message: string
  code: string
  details?: Record<string, string[]>
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  pageSize: number
  hasMore: boolean
}
```

**Usage**:
- `ApiResponse<T>`: Successful API responses
- `ApiError`: Error responses from API
- `PaginatedResponse<T>`: Future pagination support (out of scope for MVP)

## State Management

### Server State (React Query)

Managed by TanStack React Query for API data.

```typescript
// Query Keys
export const queryKeys = {
  tasks: ["tasks"] as const,
  task: (id: string) => ["tasks", id] as const,
  user: ["user"] as const,
}

// Query Functions
export const taskQueries = {
  all: () => ({
    queryKey: queryKeys.tasks,
    queryFn: () => api.get<Task[]>("/api/v1/tasks"),
    staleTime: 5000, // 5 seconds
  }),

  byId: (id: string) => ({
    queryKey: queryKeys.task(id),
    queryFn: () => api.get<Task>(`/api/v1/tasks/${id}`),
    staleTime: 5000,
  }),
}
```

**Cache Strategy**:
- Tasks cached for 5 seconds (staleTime)
- Background refetch on window focus
- Automatic invalidation after mutations
- Optimistic updates for instant feedback

### Client State (React Context)

Managed by React Context for UI state.

```typescript
// contexts/TaskFilterContext.tsx

export interface TaskFilterContextValue {
  filter: TaskFilter
  setFilter: (filter: TaskFilter) => void
  searchQuery: string
  setSearchQuery: (query: string) => void
}

export const TaskFilterContext = createContext<TaskFilterContextValue | null>(null)

export function useTaskFilter() {
  const context = useContext(TaskFilterContext)
  if (!context) {
    throw new Error("useTaskFilter must be used within TaskFilterProvider")
  }
  return context
}
```

**Usage**:
- Filter state (all/active/completed)
- Search query state
- UI toggle states (modals, dropdowns)

## Data Flow Patterns

### Authentication Flow

```
1. User submits login form
   ↓
2. signIn() called with credentials
   ↓
3. Better Auth validates and creates session
   ↓
4. useAuth hook updates with user data
   ↓
5. User redirected to dashboard
```

**State Updates**:
- `Session.isLoading`: true during authentication
- `Session.user`: populated on success
- `Session.error`: populated on failure

### Task Creation Flow

```
1. User submits create task form
   ↓
2. useCreateTask mutation called
   ↓
3. Optimistic update: task added to cache immediately
   ↓
4. API request sent with JWT token
   ↓
5. On success: cache invalidated, refetch tasks
   On error: rollback optimistic update, show error
```

**State Updates**:
- Optimistic: Task added to cache with temporary ID
- Success: Cache invalidated, real task ID from server
- Error: Rollback to previous state, show error message

### Task Completion Toggle Flow

```
1. User clicks checkbox
   ↓
2. useToggleTaskComplete mutation called
   ↓
3. Optimistic update: task.completed toggled in cache
   ↓
4. API request sent with JWT token
   ↓
5. On success: cache invalidated, refetch tasks
   On error: rollback optimistic update, show error
```

**State Updates**:
- Optimistic: Task completion status toggled immediately
- Success: Cache invalidated, confirmed state from server
- Error: Rollback to previous state, show error message

### Task Filtering Flow

```
1. User selects filter (all/active/completed)
   ↓
2. setFilter() updates TaskFilterContext
   ↓
3. Task list component re-renders
   ↓
4. Filtered tasks computed from cache
   ↓
5. UI displays filtered tasks
```

**State Updates**:
- `filter`: Updated in context
- Task list: Filtered client-side (no API call)

### Task Search Flow

```
1. User types in search input
   ↓
2. setSearchQuery() updates TaskFilterContext (debounced)
   ↓
3. Task list component re-renders
   ↓
4. Filtered tasks computed from cache
   ↓
5. UI displays matching tasks
```

**State Updates**:
- `searchQuery`: Updated in context (debounced 300ms)
- Task list: Filtered client-side (no API call)

## Form State

### Login Form

```typescript
// components/auth/LoginForm.tsx

interface LoginFormData {
  email: string
  password: string
}

const loginFormSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})
```

**Validation**: Client-side validation with Zod, server-side validation on backend

### Signup Form

```typescript
// components/auth/SignupForm.tsx

interface SignupFormData {
  name: string
  email: string
  password: string
  confirmPassword: string
}

const signupFormSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email format"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[a-z]/, "Password must contain at least one lowercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
})
```

**Validation**: Client-side validation with Zod, server-side validation on backend

### Create Task Form

```typescript
// components/tasks/CreateTaskForm.tsx

interface CreateTaskFormData {
  title: string
}

const createTaskFormSchema = z.object({
  title: z.string()
    .min(1, "Task title is required")
    .max(500, "Task title must be less than 500 characters"),
})
```

**Validation**: Client-side validation with Zod, server-side validation on backend

### Edit Task Form

```typescript
// components/tasks/EditTaskForm.tsx

interface EditTaskFormData {
  title: string
}

const editTaskFormSchema = z.object({
  title: z.string()
    .min(1, "Task title is required")
    .max(500, "Task title must be less than 500 characters"),
})
```

**Validation**: Client-side validation with Zod, server-side validation on backend

## Derived State

### Filtered Tasks

```typescript
// hooks/useFilteredTasks.ts

export function useFilteredTasks() {
  const { data: tasks = [] } = useQuery(taskQueries.all())
  const { filter, searchQuery } = useTaskFilter()

  return useMemo(() => {
    let filtered = tasks

    // Apply filter
    if (filter === "active") {
      filtered = filtered.filter(task => !task.completed)
    } else if (filter === "completed") {
      filtered = filtered.filter(task => task.completed)
    }

    // Apply search
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(query)
      )
    }

    return filtered
  }, [tasks, filter, searchQuery])
}
```

**Performance**: Memoized to prevent unnecessary recalculations

### Task Statistics

```typescript
// hooks/useTaskStats.ts

export interface TaskStats {
  total: number
  active: number
  completed: number
  completionRate: number
}

export function useTaskStats(): TaskStats {
  const { data: tasks = [] } = useQuery(taskQueries.all())

  return useMemo(() => {
    const total = tasks.length
    const completed = tasks.filter(task => task.completed).length
    const active = total - completed
    const completionRate = total > 0 ? (completed / total) * 100 : 0

    return { total, active, completed, completionRate }
  }, [tasks])
}
```

**Usage**: Display task statistics in dashboard header

## Type Guards

```typescript
// types/guards.ts

export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === "object" &&
    error !== null &&
    "message" in error &&
    "code" in error
  )
}

export function isTask(value: unknown): value is Task {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "title" in value &&
    "completed" in value &&
    "userId" in value
  )
}
```

**Usage**: Runtime type checking for API responses and error handling

## Summary

This data model provides:
- **Type Safety**: Comprehensive TypeScript types for all data structures
- **Clear State Management**: Separation of server state (React Query) and client state (Context)
- **Optimistic Updates**: Instant UI feedback with rollback on error
- **Validation**: Client-side validation with Zod schemas
- **Performance**: Memoized derived state to prevent unnecessary recalculations

**Next Steps**:
- Generate API contracts in contracts/ directory
- Implement types in frontend/src/types/
- Create hooks in frontend/src/hooks/
- Build components using these types
