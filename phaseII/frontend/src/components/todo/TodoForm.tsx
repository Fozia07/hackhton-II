'use client';

import React, { useState } from 'react';
import type { TodoCreate, TodoUpdate } from '../../types/todo';

interface TodoFormProps {
  onSubmit: (data: TodoCreate | TodoUpdate) => void;
  initialValues?: TodoUpdate | null;
  isSubmitting?: boolean;
  onCancel?: () => void;
}

export const TodoForm: React.FC<TodoFormProps> = ({
  onSubmit,
  initialValues = null,
  isSubmitting = false,
  onCancel
}) => {
  const [title, setTitle] = useState(initialValues?.title || '');
  const [description, setDescription] = useState(initialValues?.description || '');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const formData = {
      title: title.trim(),
      description: description.trim() || null,
    };

    if (initialValues) {
      // For updates, only include fields that have values
      const updateData: Partial<TodoUpdate> = {};
      if (title.trim()) updateData.title = title.trim();
      if (description.trim()) updateData.description = description.trim();

      onSubmit(updateData);
    } else {
      onSubmit(formData);
    }

    // Reset form only for new todos
    if (!initialValues) {
      setTitle('');
      setDescription('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border rounded-lg p-4 bg-white shadow-sm">
      <div className="space-y-3">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full border rounded px-3 py-2 text-sm"
            placeholder="Enter todo title"
            required
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border rounded px-3 py-2 text-sm"
            placeholder="Enter todo description (optional)"
            rows={2}
          />
        </div>

        <div className="flex space-x-2 justify-end pt-2">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded"
              disabled={isSubmitting}
            >
              Cancel
            </button>
          )}
          <button
            type="submit"
            className={`px-4 py-2 text-sm text-white rounded ${
              isSubmitting ? 'bg-blue-400' : 'bg-blue-500 hover:bg-blue-600'
            }`}
            disabled={isSubmitting || !title.trim()}
          >
            {initialValues ? 'Update Todo' : 'Create Todo'}
          </button>
        </div>
      </div>
    </form>
  );
};