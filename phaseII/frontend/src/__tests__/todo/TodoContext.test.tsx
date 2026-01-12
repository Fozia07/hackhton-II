import React from 'react';
import { render, act, waitFor } from '@testing-library/react';
import { TodoProvider, useTodo } from '@/contexts/TodoContext';
import { Todo } from '@/types/todo';

// Mock the todoService
jest.mock('@/lib/todo/service', () => ({
  todoService: {
    getAllTodos: jest.fn(),
    createTodo: jest.fn(),
    updateTodo: jest.fn(),
    deleteTodo: jest.fn(),
  },
}));

const { todoService } = require('@/lib/todo/service');

// Helper component to access the context
const TestComponent: React.FC = () => {
  const { state, createTodo, updateTodo, deleteTodo, fetchTodos } = useTodo();

  return (
    <div>
      <div data-testid="loading">{String(state.isLoading)}</div>
      <div data-testid="error">{state.error || 'no-error'}</div>
      <div data-testid="todo-count">{state.todos.length}</div>
      <button data-testid="fetch-btn" onClick={fetchTodos}>Fetch</button>
      <button data-testid="create-btn" onClick={() => createTodo({ title: 'Test', description: 'Test desc' })}>
        Create
      </button>
    </div>
  );
};

const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <TodoProvider>{children}</TodoProvider>
);

describe('TodoContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with default state', () => {
    const { getByTestId } = render(
      <Wrapper>
        <TestComponent />
      </Wrapper>
    );

    expect(getByTestId('loading').textContent).toBe('false');
    expect(getByTestId('error').textContent).toBe('no-error');
    expect(getByTestId('todo-count').textContent).toBe('0');
  });

  it('should fetch todos successfully', async () => {
    const mockTodos: Todo[] = [
      {
        id: 1,
        title: 'Test Todo',
        description: 'Test Description',
        completed: false,
        user_id: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];

    (todoService.getAllTodos as jest.MockedFunction<any>).mockResolvedValue({
      data: mockTodos,
      status: 200,
    });

    const { getByTestId } = render(
      <Wrapper>
        <TestComponent />
      </Wrapper>
    );

    await act(async () => {
      getByTestId('fetch-btn').click();
    });

    await waitFor(() => {
      expect(getByTestId('todo-count').textContent).toBe('1');
    });
  });

  it('should handle fetch todos error', async () => {
    (todoService.getAllTodos as jest.MockedFunction<any>).mockResolvedValue({
      error: 'Network error',
      status: 500,
    });

    const { getByTestId } = render(
      <Wrapper>
        <TestComponent />
      </Wrapper>
    );

    await act(async () => {
      getByTestId('fetch-btn').click();
    });

    await waitFor(() => {
      expect(getByTestId('error').textContent).toBe('Network error');
    });
  });

  it('should create a new todo', async () => {
    const newTodo: Todo = {
      id: 1,
      title: 'New Todo',
      description: 'New Description',
      completed: false,
      user_id: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    (todoService.createTodo as jest.MockedFunction<any>).mockResolvedValue({
      data: newTodo,
      status: 201,
    });

    const { getByTestId } = render(
      <Wrapper>
        <TestComponent />
      </Wrapper>
    );

    await act(async () => {
      getByTestId('create-btn').click();
    });

    await waitFor(() => {
      expect(getByTestId('todo-count').textContent).toBe('1');
    });
  });
});