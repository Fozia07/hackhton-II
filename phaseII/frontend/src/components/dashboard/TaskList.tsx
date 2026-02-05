'use client';

import React from 'react';
import { TaskItem } from './TaskItem';
import type { Todo } from '@/types/todo';

interface TaskListProps {
  tasks: Todo[];
  activeTab: string;
  onToggleComplete: (id: number) => void;
  onEdit: (task: Todo) => void;
  onDelete: (id: number) => void;
  className?: string;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  activeTab,
  onToggleComplete,
  onEdit,
  onDelete,
  className
}) => {
  // Filter tasks based on active tab
  const filteredTasks = tasks.filter(task => {
    switch (activeTab) {
      case 'all':
        return true; // Show all tasks
      case 'active':
        return !task.completed; // Show only active (non-completed) tasks
      case 'completed':
        return task.completed; // Show only completed tasks
      default:
        return true; // Default to show all tasks
    }
  });

  if (filteredTasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto h-12 w-12 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-1">No tasks found</h3>
        <p className="text-gray-500 dark:text-gray-400">
          {activeTab === 'all'
            ? 'No tasks available'
            : activeTab === 'active'
              ? 'No active tasks'
              : 'No completed tasks'}
        </p>
      </div>
    );
  }

  return (
    <div className={`space-y-3 ${className}`}>
      {filteredTasks.map((task) => (
        <TaskItem
          key={task.id}
          id={task.id}
          title={task.title}
          description={task.description || ''}
          completed={task.completed}
          onToggleComplete={onToggleComplete}
          onEdit={() => onEdit(task)}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export { TaskList };