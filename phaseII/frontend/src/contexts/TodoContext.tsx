'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import type { Todo, TodoCreate, TodoUpdate, TodoState } from '../types/todo';
import { todoService } from '../lib/todo/service';

type TodoAction =
  | { type: 'FETCH_TODOS_START' }
  | { type: 'FETCH_TODOS_SUCCESS'; payload: Todo[] }
  | { type: 'FETCH_TODOS_ERROR'; payload: string }
  | { type: 'CREATE_TODO_START' }
  | { type: 'CREATE_TODO_SUCCESS'; payload: Todo }
  | { type: 'CREATE_TODO_ERROR'; payload: string }
  | { type: 'UPDATE_TODO_START' }
  | { type: 'UPDATE_TODO_SUCCESS'; payload: Todo }
  | { type: 'UPDATE_TODO_ERROR'; payload: string }
  | { type: 'DELETE_TODO_START' }
  | { type: 'DELETE_TODO_SUCCESS'; payload: number }
  | { type: 'DELETE_TODO_ERROR'; payload: string }
  | { type: 'SET_SELECTED_TODO'; payload: Todo | null };

const initialState: TodoState = {
  todos: [],
  isLoading: false,
  error: null,
  selectedTodo: null,
};

const TodoContext = createContext<{
  state: TodoState;
  fetchTodos: () => Promise<void>;
  createTodo: (todoData: TodoCreate) => Promise<void>;
  updateTodo: (id: number, todoData: Partial<TodoUpdate>) => Promise<void>;
  deleteTodo: (id: number) => Promise<void>;
  setSelectedTodo: (todo: Todo | null) => void;
}>({
  state: initialState,
  fetchTodos: async () => {},
  createTodo: async () => {},
  updateTodo: async () => {},
  deleteTodo: async () => {},
  setSelectedTodo: () => {},
});

const todoReducer = (state: TodoState, action: TodoAction): TodoState => {
  switch (action.type) {
    case 'FETCH_TODOS_START':
      return { ...state, isLoading: true, error: null };
    case 'FETCH_TODOS_SUCCESS':
      return { ...state, isLoading: false, todos: action.payload, error: null };
    case 'FETCH_TODOS_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'CREATE_TODO_START':
      return { ...state, isLoading: true, error: null };
    case 'CREATE_TODO_SUCCESS':
      return {
        ...state,
        isLoading: false,
        todos: [...state.todos, action.payload],
        error: null,
      };
    case 'CREATE_TODO_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'UPDATE_TODO_START':
      return { ...state, isLoading: true, error: null };
    case 'UPDATE_TODO_SUCCESS':
      return {
        ...state,
        isLoading: false,
        todos: state.todos.map(todo =>
          todo.id === action.payload.id ? action.payload : todo
        ),
        error: null,
      };
    case 'UPDATE_TODO_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'DELETE_TODO_START':
      return { ...state, isLoading: true, error: null };
    case 'DELETE_TODO_SUCCESS':
      return {
        ...state,
        isLoading: false,
        todos: state.todos.filter(todo => todo.id !== action.payload),
        error: null,
      };
    case 'DELETE_TODO_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'SET_SELECTED_TODO':
      return { ...state, selectedTodo: action.payload };
    default:
      return state;
  }
};

interface TodoProviderProps {
  children: React.ReactNode;
  authState?: {
    isAuthenticated: boolean;
    isLoading: boolean;
  };
}

export const TodoProvider: React.FC<TodoProviderProps> = ({ children, authState }) => {
  const [state, dispatch] = useReducer(todoReducer, initialState);

  const fetchTodos = async () => {
    // Only fetch if user is authenticated
    if (authState && !authState.isAuthenticated) {
      return;
    }

    dispatch({ type: 'FETCH_TODOS_START' });
    try {
      const response = await todoService.getAllTodos();
      if (response.data) {
        dispatch({ type: 'FETCH_TODOS_SUCCESS', payload: response.data });
      } else {
        dispatch({ type: 'FETCH_TODOS_ERROR', payload: response.error || 'Failed to fetch todos' });
      }
    } catch (error: any) {
      dispatch({ type: 'FETCH_TODOS_ERROR', payload: error.message });
    }
  };

  const createTodo = async (todoData: TodoCreate) => {
    // Only allow creation if user is authenticated
    if (authState && !authState.isAuthenticated) {
      dispatch({ type: 'CREATE_TODO_ERROR', payload: 'User not authenticated' });
      return;
    }

    dispatch({ type: 'CREATE_TODO_START' });
    try {
      console.log('Creating todo with data:', todoData);
      const response = await todoService.createTodo(todoData);
      console.log('Create todo response:', response);
      if (response.data) {
        console.log('Todo created successfully:', response.data);
        dispatch({ type: 'CREATE_TODO_SUCCESS', payload: response.data });
      } else {
        console.error('Failed to create todo:', response.error);
        dispatch({ type: 'CREATE_TODO_ERROR', payload: response.error || 'Failed to create todo' });
      }
    } catch (error: any) {
      console.error('Error creating todo:', error);
      dispatch({ type: 'CREATE_TODO_ERROR', payload: error.message });
    }
  };

  const updateTodo = async (id: number, todoData: Partial<TodoUpdate>) => {
    // Only allow update if user is authenticated
    if (authState && !authState.isAuthenticated) {
      dispatch({ type: 'UPDATE_TODO_ERROR', payload: 'User not authenticated' });
      return;
    }

    dispatch({ type: 'UPDATE_TODO_START' });
    try {
      const response = await todoService.updateTodo(id, todoData);
      if (response.data) {
        dispatch({ type: 'UPDATE_TODO_SUCCESS', payload: response.data });
      } else {
        // Ensure error message is a string, not an object
        const errorMessage = response.error ?
          typeof response.error === 'string' ? response.error :
          JSON.stringify(response.error) :
          'Failed to update todo';
        dispatch({ type: 'UPDATE_TODO_ERROR', payload: errorMessage });
      }
    } catch (error: any) {
      // Ensure error message is a string, not an object
      const errorMessage = error.message ?
        typeof error.message === 'string' ? error.message :
        JSON.stringify(error.message) :
        'An unknown error occurred while updating the todo';
      dispatch({ type: 'UPDATE_TODO_ERROR', payload: errorMessage });
    }
  };

  const deleteTodo = async (id: number) => {
    // Only allow deletion if user is authenticated
    if (authState && !authState.isAuthenticated) {
      dispatch({ type: 'DELETE_TODO_ERROR', payload: 'User not authenticated' });
      return;
    }

    dispatch({ type: 'DELETE_TODO_START' });
    try {
      const response = await todoService.deleteTodo(id);
      if (response.data) {
        dispatch({ type: 'DELETE_TODO_SUCCESS', payload: id });
      } else {
        dispatch({ type: 'DELETE_TODO_ERROR', payload: response.error || 'Failed to delete todo' });
      }
    } catch (error: any) {
      dispatch({ type: 'DELETE_TODO_ERROR', payload: error.message });
    }
  };

  const setSelectedTodo = (todo: Todo | null) => {
    dispatch({ type: 'SET_SELECTED_TODO', payload: todo });
  };

  // Fetch todos on initial load only if authenticated
  useEffect(() => {
    if (authState && authState.isAuthenticated && !authState.isLoading) {
      fetchTodos();
    }
  }, [authState?.isAuthenticated, authState?.isLoading]);

  return (
    <TodoContext.Provider
      value={{
        state,
        fetchTodos,
        createTodo,
        updateTodo,
        deleteTodo,
        setSelectedTodo,
      }}
    >
      {children}
    </TodoContext.Provider>
  );
};

export const useTodo = () => {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodo must be used within a TodoProvider');
  }
  return context;
};