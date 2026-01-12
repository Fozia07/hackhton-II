'use client';

import React, { useState } from 'react';
import { Todo, TodoUpdate } from '../../types/todo';

interface TodoItemProps {
  todo: Todo;
  onEdit: () => void;
  onDelete: () => void;
  onUpdate: (id: number, data: Partial<TodoUpdate>) => void;
}

export const TodoItem: React.FC<TodoItemProps> = ({ todo, onEdit, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(todo.title);
  const [description, setDescription] = useState(todo.description || '');

  const handleSave = () => {
    onUpdate(todo.id, { title, description: description || null });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(todo.title);
    setDescription(todo.description || '');
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    onUpdate(todo.id, { completed: !todo.completed });
  };

  return (
    <div className={`border rounded-lg p-4 shadow-sm ${todo.completed ? 'bg-green-50' : 'bg-white'}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full border rounded px-3 py-2 text-sm"
            placeholder="Todo title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border rounded px-3 py-2 text-sm"
            placeholder="Todo description (optional)"
            rows={2}
          />
          <div className="flex space-x-2 justify-end">
            <button
              onClick={handleCancel}
              className="px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 rounded"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-3 py-1 text-sm bg-blue-500 text-white hover:bg-blue-600 rounded"
            >
              Save
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggleComplete}
              className="mt-1 h-4 w-4"
            />
            <div className="flex-1">
              <h3 className={`font-medium ${todo.completed ? 'line-through text-gray-500' : ''}`}>
                {todo.title}
              </h3>
              {todo.description && (
                <p className={`text-sm mt-1 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                  {todo.description}
                </p>
              )}
              <div className="text-xs text-gray-400 mt-2">
                Created: {new Date(todo.created_at).toLocaleDateString()}
              </div>
            </div>
            <div className="flex space-x-1">
              <button
                onClick={onEdit}
                className="text-blue-500 hover:text-blue-700 text-sm"
              >
                Edit
              </button>
              <button
                onClick={onDelete}
                className="text-red-500 hover:text-red-700 text-sm ml-2"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};