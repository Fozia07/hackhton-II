'use client';

import React from 'react';
import type { Todo, TodoUpdate } from '../../types/todo';
import { TodoItem } from './TodoItem';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

interface TodoListProps {
  todos: Todo[];
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => void;
  onUpdate: (id: number, data: Partial<TodoUpdate>) => void;
}

export const TodoList: React.FC<TodoListProps> = ({ todos, onEdit, onDelete, onUpdate }) => {
  const reducedMotion = useReducedMotion();

  if (todos.length === 0) {
    return (
      <motion.div
        initial={reducedMotion ? {} : { opacity: 0, scale: 0.95 }}
        animate={reducedMotion ? {} : { opacity: 1, scale: 1 }}
        transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        className="text-center py-12"
      >
        <div className="mx-auto h-24 w-24 rounded-full bg-primary-50 dark:bg-primary-900/20 flex items-center justify-center mb-4 shadow-[var(--shadow-sm)]">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold mb-1 text-foreground">No tasks yet</h3>
        <p className="text-muted-foreground">
          Get started by creating your first task
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={reducedMotion ? {} : { opacity: 0 }}
      animate={reducedMotion ? {} : { opacity: 1 }}
      transition={reducedMotion ? {} : { duration: 0.3 }}
      className="space-y-3"
    >
      <AnimatePresence mode="popLayout">
        {todos.map((todo, index) => (
          <motion.div
            key={todo.id}
            initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
            animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
            exit={reducedMotion ? {} : { opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
            transition={reducedMotion ? {} : { delay: index * 0.05, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            layout
          >
            <TodoItem
              todo={todo}
              onEdit={() => onEdit(todo)}
              onDelete={() => onDelete(todo.id)}
              onUpdate={onUpdate}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </motion.div>
  );
};