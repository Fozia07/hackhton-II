'use client';

import React, { useState } from 'react';
import type { TodoCreate, TodoUpdate } from '../../types/todo';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

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
  const reducedMotion = useReducedMotion();
  const [title, setTitle] = useState(initialValues?.title || '');
  const [description, setDescription] = useState(initialValues?.description || '');
  const [error, setError] = useState('');

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
    <motion.form
      initial={reducedMotion ? {} : { opacity: 0, y: 10 }}
      animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
      transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      onSubmit={handleSubmit}
      className="rounded-xl border border-border bg-card p-6 shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-md)] transition-shadow duration-250"
    >
      <div className="space-y-5">
        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, x: -10 }}
          animate={reducedMotion ? {} : { opacity: 1, x: 0 }}
          transition={reducedMotion ? {} : { delay: 0.1, duration: 0.3 }}
        >
          <label htmlFor="title" className="mb-2 block text-sm font-semibold text-foreground">
            Title <span className="text-error-600 dark:text-error-400">*</span>
          </label>
          <Input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter todo title"
            required
            disabled={isSubmitting}
            className="w-full transition-all duration-200"
          />
        </motion.div>

        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, x: -10 }}
          animate={reducedMotion ? {} : { opacity: 1, x: 0 }}
          transition={reducedMotion ? {} : { delay: 0.15, duration: 0.3 }}
        >
          <label htmlFor="description" className="mb-2 block text-sm font-semibold text-foreground">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter todo description (optional)"
            rows={3}
            disabled={isSubmitting}
            className="flex w-full rounded-md border-2 border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 dark:focus-visible:ring-primary-500 focus-visible:ring-offset-2 focus-visible:border-primary-400 dark:focus-visible:border-primary-500 hover:border-primary-300 dark:hover:border-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
          />
        </motion.div>

        <AnimatePresence>
          {error && (
            <motion.div
              initial={reducedMotion ? {} : { opacity: 0, y: -10 }}
              animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
              exit={reducedMotion ? {} : { opacity: 0, y: -10 }}
              className="rounded-lg bg-error-50 dark:bg-error-900/20 border border-error-200 dark:border-error-800 px-4 py-3 text-sm text-error-700 dark:text-error-400"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, y: 10 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { delay: 0.2, duration: 0.3 }}
          className="flex justify-end space-x-3 pt-2"
        >
          {onCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
          )}
          <Button
            type="submit"
            disabled={isSubmitting || !title.trim()}
            className="min-w-[120px]"
          >
            {isSubmitting ? (
              <motion.div
                initial={reducedMotion ? {} : { opacity: 0 }}
                animate={reducedMotion ? {} : { opacity: 1 }}
                className="flex items-center"
              >
                <svg className="mr-2 h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {initialValues ? 'Updating...' : 'Creating...'}
              </motion.div>
            ) : (
              `${initialValues ? 'Update' : 'Create'} Todo`
            )}
          </Button>
        </motion.div>
      </div>
    </motion.form>
  );
};