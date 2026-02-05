'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { useTodo } from '@/contexts/TodoContext';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { TabNavigation } from '@/components/dashboard/TabNavigation';
import { TaskList } from '@/components/dashboard/TaskList';
import { TodoForm } from '@/components/todo/TodoForm';

export default function DashboardPage() {
  const [mounted, setMounted] = useState(false);
  const [activeTab, setActiveTab] = useState('today');
  const { state, createTodo, updateTodo, deleteTodo, setSelectedTodo } = useTodo();
  const [showAddForm, setShowAddForm] = useState(false);
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  const handleCreateTodo = async (data: any) => {
    await createTodo(data);
    setShowAddForm(false);
  };

  const handleDeleteTodo = async (id: number) => {
    await deleteTodo(id);
  };

  const handleEditTodo = (todo: any) => {
    setSelectedTodo(todo);
    setShowAddForm(true);
  };

  const handleUpdateTodo = async (id: number, data: any) => {
    await updateTodo(id, data);
    setShowAddForm(false);
  };

  const handleCancelEdit = () => {
    setSelectedTodo(null);
    setShowAddForm(false);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header Section */}
      <motion.section
        initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
        animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
        transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        className="bg-gradient-to-r from-primary-500 to-secondary-500 dark:from-primary-600 dark:to-secondary-600 rounded-xl p-6 text-white"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-2">Todo App</h1>
        <p className="text-primary-100 dark:text-primary-200">
          Manage your tasks efficiently and boost your productivity
        </p>
      </motion.section>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { delay: 0.1, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="bg-card border border-border rounded-lg p-4 shadow-[var(--shadow-sm)]">
            <h3 className="text-lg font-semibold text-foreground">Total Tasks</h3>
            <div className="text-3xl font-bold text-primary-600 dark:text-primary-400 mt-1">{state.todos.length}</div>
            <p className="text-sm text-muted-foreground mt-1">All tasks in your list</p>
          </div>
        </motion.div>

        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { delay: 0.15, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="bg-card border border-border rounded-lg p-4 shadow-[var(--shadow-sm)]">
            <h3 className="text-lg font-semibold text-foreground">Active</h3>
            <div className="text-3xl font-bold text-secondary-600 dark:text-secondary-400 mt-1">
              {state.todos.filter(t => !t.completed).length}
            </div>
            <p className="text-sm text-muted-foreground mt-1">Tasks to complete</p>
          </div>
        </motion.div>

        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { delay: 0.2, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="bg-card border border-border rounded-lg p-4 shadow-[var(--shadow-sm)]">
            <h3 className="text-lg font-semibold text-foreground">Completed</h3>
            <div className="text-3xl font-bold text-success-600 dark:text-success-400 mt-1">
              {state.todos.filter(t => t.completed).length}
            </div>
            <p className="text-sm text-muted-foreground mt-1">Tasks finished</p>
          </div>
        </motion.div>
      </div>

      {/* Add Task Form */}
      {showAddForm && (
        <motion.section
          initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="bg-card border border-border rounded-lg p-6 shadow-[var(--shadow-md)]">
            <h2 className="text-xl font-semibold text-foreground mb-4">
              {state.selectedTodo ? 'Edit Task' : 'Add New Task'}
            </h2>
            <TodoForm
              initialValues={state.selectedTodo || undefined}
              onSubmit={state.selectedTodo ? (data) => handleUpdateTodo(state.selectedTodo!.id, data) : handleCreateTodo}
              onCancel={handleCancelEdit}
              isSubmitting={state.isLoading}
            />
          </div>
        </motion.section>
      )}

      {/* Task Section with Tabs */}
      <motion.section
        initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
        animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
        transition={reducedMotion ? {} : { delay: 0.25, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      >
        <div className="bg-card border border-border rounded-lg p-6 shadow-[var(--shadow-md)]">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-foreground">Tasks</h2>
            <Button
              variant="success"
              onClick={() => {
                setSelectedTodo(null);
                setShowAddForm(true);
              }}
            >
              + Add Task
            </Button>
          </div>

          <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />

          <div className="mt-6">
            <TaskList
              tasks={state.todos}
              activeTab={activeTab}
              onToggleComplete={async (id: number) => {
                const task = state.todos.find(t => t.id === id);
                if (task) {
                  await updateTodo(id, { completed: !task.completed });
                }
              }}
              onEdit={handleEditTodo}
              onDelete={handleDeleteTodo}
            />
          </div>
        </div>
      </motion.section>
    </div>
  );
}