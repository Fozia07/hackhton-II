import type { Todo, TodoCreate, TodoUpdate } from '../../types/todo';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

class TodoService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('auth_token');
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  }

  async getAllTodos(): Promise<ApiResponse<Todo[]>> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/todos`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });

      // Check if the response is ok before parsing JSON
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;

        // If it's an authentication error, the token might be expired
        if (response.status === 401 || response.status === 403) {
          // Optionally clear the token if it's invalid
          // localStorage.removeItem('auth_token');
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();
      return { data, status: response.status };
    } catch (error: any) {
      // Handle network errors and other exceptions
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return { error: 'Network error: Failed to connect to server', status: 500 };
      }
      return { error: error.message, status: 500 };
    }
  }

  async createTodo(todoData: TodoCreate): Promise<ApiResponse<Todo>> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/todos`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(todoData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;

        if (response.status === 401 || response.status === 403) {
          // Authentication error
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();
      return { data, status: response.status };
    } catch (error: any) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return { error: 'Network error: Failed to connect to server', status: 500 };
      }
      return { error: error.message, status: 500 };
    }
  }

  async updateTodo(id: number, todoData: Partial<TodoUpdate>): Promise<ApiResponse<Todo>> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(todoData),
      });

      if (!response.ok) {
        // Try to parse the error response properly
        let errorMessage = `HTTP error! status: ${response.status}`;

        try {
          const errorData = await response.json();
          // Handle different possible error response formats
          if (errorData.detail) {
            errorMessage = typeof errorData.detail === 'string'
              ? errorData.detail
              : JSON.stringify(errorData.detail);
          } else if (errorData.message) {
            errorMessage = errorData.message;
          } else if (Array.isArray(errorData)) {
            // Handle validation errors array
            errorMessage = errorData.map(err => err.msg || err.detail || JSON.stringify(err)).join('; ');
          }
        } catch (parseError) {
          // If we can't parse the error response, use status text
          errorMessage = response.statusText || errorMessage;
        }

        if (response.status === 401 || response.status === 403) {
          // Authentication error
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();
      return { data, status: response.status };
    } catch (error: any) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return { error: 'Network error: Failed to connect to server', status: 500 };
      }
      return { error: error.message, status: 500 };
    }
  }

  async deleteTodo(id: number): Promise<ApiResponse<{ message: string }>> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;

        if (response.status === 401 || response.status === 403) {
          // Authentication error
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();
      return { data, status: response.status };
    } catch (error: any) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return { error: 'Network error: Failed to connect to server', status: 500 };
      }
      return { error: error.message, status: 500 };
    }
  }
}

export const todoService = new TodoService();