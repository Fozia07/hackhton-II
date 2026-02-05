'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';

interface TaskItemProps {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  onToggleComplete: (id: number) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  className?: string;
}

const TaskItem: React.FC<TaskItemProps> = ({
  id,
  title,
  description,
  completed,
  onToggleComplete,
  onEdit,
  onDelete,
  className
}) => {
  return (
    <div
      className={cn(
        'flex items-center justify-between p-4 border rounded-lg transition-all duration-200 hover:shadow-sm hover:border-primary-200 dark:hover:border-primary-700',
        completed ? 'bg-green-50/30 dark:bg-green-900/10' : 'bg-white dark:bg-gray-800',
        className
      )}
    >
      <div className="flex items-center space-x-3 flex-1 min-w-0">
        <Checkbox
          id={`task-${id}`}
          checked={completed}
          onCheckedChange={() => onToggleComplete(id)}
          className="data-[state=checked]:bg-success-600 data-[state=checked]:text-white"
        />
        <div className="flex-1 min-w-0">
          <h3
            className={cn(
              'font-medium truncate',
              completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-900 dark:text-gray-100'
            )}
          >
            {title}
          </h3>
          {description && (
            <p className="text-sm text-gray-500 dark:text-gray-400 truncate mt-1">
              {description}
            </p>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-2 ml-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => onEdit(id)}
          className="h-8 w-8 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400"
          aria-label="Edit task"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
          </svg>
        </Button>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => onDelete(id)}
          className="h-8 w-8 text-gray-600 dark:text-gray-300 hover:text-error-600 dark:hover:text-error-400"
          aria-label="Delete task"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 6h18"/>
            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
          </svg>
        </Button>
      </div>
    </div>
  );
};

export { TaskItem };