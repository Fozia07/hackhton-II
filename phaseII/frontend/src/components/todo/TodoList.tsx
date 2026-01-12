'use client';

import React from 'react';
import { Todo, TodoUpdate } from '../types/todo';
import { TodoItem } from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => void;
  onUpdate: (id: number, data: Partial<TodoUpdate>) => void;
}

export const TodoList: React.FC<TodoListProps> = ({ todos, onEdit, onDelete, onUpdate }) => {
  if (todos.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No todos yet. Create your first todo!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onEdit={() => onEdit(todo)}
          onDelete={() => onDelete(todo.id)}
          onUpdate={onUpdate}
        />
      ))}
    </div>
  );
};