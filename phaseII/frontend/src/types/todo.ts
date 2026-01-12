export interface Todo {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: number;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

export interface TodoCreate {
  title: string;
  description?: string | null;
}

export interface TodoUpdate {
  title?: string;
  description?: string | null;
  completed?: boolean;
}

export interface TodoState {
  todos: Todo[];
  isLoading: boolean;
  error: string | null;
  selectedTodo: Todo | null;
}