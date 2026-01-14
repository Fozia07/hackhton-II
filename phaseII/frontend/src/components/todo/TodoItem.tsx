'use client';

import React, { useState } from 'react';
import type { Todo, TodoUpdate } from '../../types/todo';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useReducedMotion } from '@/hooks/useReducedMotion';

interface TodoItemProps {
  todo: Todo;
  onEdit: () => void;
  onDelete: () => void;
  onUpdate: (id: number, data: Partial<TodoUpdate>) => void;
}

export const TodoItem: React.FC<TodoItemProps> = ({ todo, onEdit, onDelete, onUpdate }) => {
  const reducedMotion = useReducedMotion();
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
    <motion.div
      initial={reducedMotion ? {} : { opacity: 0, y: 10 }}
      animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
      exit={reducedMotion ? {} : { opacity: 0, y: -10 }}
      whileHover={reducedMotion ? {} : { scale: 1.01, y: -2 }}
      layout
      className={`group relative rounded-xl border p-5 transition-all duration-250 ${
        todo.completed
          ? 'bg-success-50/50 dark:bg-success-900/10 border-success-300 dark:border-success-700 shadow-[var(--shadow-sm)]'
          : 'bg-card border-border shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-md)] hover:border-primary-200 dark:hover:border-primary-700'
      }`}
    >
      {isEditing ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-4"
        >
          <Input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full"
            placeholder="Todo title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            placeholder="Todo description (optional)"
            rows={2}
          />
          <div className="flex justify-end space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCancel}
            >
              Cancel
            </Button>
            <Button
              size="sm"
              onClick={handleSave}
            >
              Save
            </Button>
          </div>
        </motion.div>
      ) : (
        <div className="flex items-start gap-3">
          <motion.div
            className="relative flex h-6 w-6 shrink-0 items-center justify-center"
            whileHover={reducedMotion ? {} : { scale: 1.1 }}
            whileTap={reducedMotion ? {} : { scale: 0.95 }}
          >
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggleComplete}
              className="peer h-6 w-6 cursor-pointer appearance-none rounded-md border-2 border-primary-400 dark:border-primary-500 bg-background align-middle transition-all duration-200 hover:border-primary-600 dark:hover:border-primary-400 hover:shadow-[var(--shadow-sm)] checked:bg-primary-600 dark:checked:bg-primary-500 checked:border-primary-600 dark:checked:border-primary-500"
            />
            <svg
              className="pointer-events-none absolute left-1/2 top-1/2 h-4 w-4 -translate-x-1/2 -translate-y-1/2 text-white opacity-0 transition-all duration-200 peer-checked:opacity-100"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="3"
            >
              <path d="M5.85 12.85L9.5 16.5L18.5 7.5" />
            </svg>
          </motion.div>

          <div className="flex-1 min-w-0">
            <h3 className={`font-medium truncate ${todo.completed ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
              {todo.title}
            </h3>
            {todo.description && (
              <p className={`text-sm mt-1 truncate ${todo.completed ? 'line-through text-muted-foreground' : 'text-muted-foreground'}`}>
                {todo.description}
              </p>
            )}
            <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
              <span>Created: {new Date(todo.created_at).toLocaleDateString()}</span>
              {todo.completed && (
                <span className="inline-flex items-center rounded-full bg-success-100 dark:bg-success-900/30 px-2.5 py-0.5 text-xs font-medium text-success-700 dark:text-success-400 border border-success-200 dark:border-success-800">
                  Completed
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-all duration-200">
            <motion.div whileHover={reducedMotion ? {} : { scale: 1.1 }} whileTap={reducedMotion ? {} : { scale: 0.95 }}>
              <Button
                variant="ghost"
                size="sm"
                onClick={onEdit}
                className="h-9 w-9 p-0 text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 hover:text-primary-700 dark:hover:text-primary-300 border border-transparent hover:border-primary-200 dark:hover:border-primary-800 hover:shadow-[var(--shadow-sm)]"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </Button>
            </motion.div>
            <motion.div whileHover={reducedMotion ? {} : { scale: 1.1 }} whileTap={reducedMotion ? {} : { scale: 0.95 }}>
              <Button
                variant="ghost"
                size="sm"
                onClick={onDelete}
                className="h-9 w-9 p-0 text-error-600 dark:text-error-400 hover:bg-error-50 dark:hover:bg-error-900/20 hover:text-error-700 dark:hover:text-error-300 border border-transparent hover:border-error-200 dark:hover:border-error-800 hover:shadow-[var(--shadow-sm)]"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </Button>
            </motion.div>
          </div>
        </div>
      )}
    </motion.div>
  );
};