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

export type TaskFilter = 'all' | 'active' | 'completed'

export interface TaskListState {
  tasks: Task[]
  filter: TaskFilter
  searchQuery: string
  isLoading: boolean
  error: Error | null
}