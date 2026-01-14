'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { useTodo } from '@/contexts/TodoContext';
import { TodoList } from '@/components/todo/TodoList';
import { TodoForm } from '@/components/todo/TodoForm';
import { useReducedMotion } from '@/hooks/useReducedMotion';

export default function DashboardPage() {
  const [mounted, setMounted] = useState(false);
  const { state, createTodo, updateTodo, deleteTodo, setSelectedTodo } = useTodo();
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  const handleCreateTodo = async (data: any) => {
    await createTodo(data);
  };

  const handleDeleteTodo = async (id: number) => {
    await deleteTodo(id);
  };

  const handleEditTodo = (todo: any) => {
    setSelectedTodo(todo);
  };

  const handleUpdateTodo = async (id: number, data: any) => {
    await updateTodo(id, data);
  };

  const handleCancelEdit = () => {
    setSelectedTodo(null);
  };

  const filteredTodos = state.selectedTodo ? [state.selectedTodo] : state.todos;

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Welcome Section */}
      <motion.section
        initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
        animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
        transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 via-primary-500 to-secondary-600 dark:from-primary-400 dark:via-primary-300 dark:to-secondary-400 mb-4">
          Welcome Back!
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Manage your tasks efficiently and boost your productivity with our beautiful and intuitive interface.
        </p>
      </motion.section>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
            animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
            transition={reducedMotion ? {} : { delay: 0.1, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          >
            <Card className="bg-card border border-border shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-md)] transition-all duration-250">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl font-semibold text-foreground">Total Tasks</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-primary-600 dark:text-primary-400">{state.todos.length}</div>
                <p className="text-sm text-muted-foreground mt-1">All tasks in your list</p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
            animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
            transition={reducedMotion ? {} : { delay: 0.15, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          >
            <Card className="bg-card border border-border shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-md)] transition-all duration-250">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl font-semibold text-foreground">Active</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-secondary-600 dark:text-secondary-400">
                  {state.todos.filter(t => !t.completed).length}
                </div>
                <p className="text-sm text-muted-foreground mt-1">Tasks to complete</p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
            animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
            transition={reducedMotion ? {} : { delay: 0.2, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          >
            <Card className="bg-card border border-border shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-md)] transition-all duration-250">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl font-semibold text-foreground">Completed</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-success-600 dark:text-success-400">
                  {state.todos.filter(t => t.completed).length}
                </div>
                <p className="text-sm text-muted-foreground mt-1">Tasks finished</p>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Todo Form */}
        <motion.section
          initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { delay: 0.25, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        >
          <Card className="bg-card border border-border shadow-[var(--shadow-md)]">
            <CardHeader>
              <CardTitle className="text-xl font-semibold text-foreground">
                {state.selectedTodo ? 'Edit Todo' : 'Create New Todo'}
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                {state.selectedTodo
                  ? 'Update your existing task'
                  : 'Add a new task to your list'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {state.selectedTodo ? (
                <TodoForm
                  initialValues={state.selectedTodo}
                  onSubmit={(data) => handleUpdateTodo(state.selectedTodo!.id, data)}
                  onCancel={handleCancelEdit}
                  isSubmitting={state.isLoading}
                />
              ) : (
                <TodoForm
                  onSubmit={handleCreateTodo}
                  isSubmitting={state.isLoading}
                />
              )}
            </CardContent>
          </Card>
        </motion.section>

        {/* Todo List */}
        <motion.section
          initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { delay: 0.3, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        >
          <Card className="bg-card border border-border shadow-[var(--shadow-md)]">
            <CardHeader>
              <CardTitle className="text-xl font-semibold text-foreground">Your Tasks</CardTitle>
              <CardDescription className="text-muted-foreground">
                {state.todos.length} {state.todos.length === 1 ? 'task' : 'tasks'} in your list
              </CardDescription>
            </CardHeader>
            <CardContent>
              {state.isLoading ? (
                <div className="flex justify-center items-center h-32">
                  <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600"></div>
                </div>
              ) : state.error ? (
                <div className="text-center py-8">
                  <p className="text-error-600 dark:text-error-500">Error: {state.error}</p>
                  <Button
                    onClick={() => window.location.reload()}
                    className="mt-4"
                  >
                    Refresh
                  </Button>
                </div>
              ) : filteredTodos.length === 0 ? (
                <div className="text-center py-12">
                  <div className="mx-auto h-24 w-24 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center mb-4 shadow-[var(--shadow-sm)]">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold mb-1 text-foreground">No tasks yet</h3>
                  <p className="text-muted-foreground mb-4">
                    {state.selectedTodo
                      ? 'Selected task not found'
                      : 'Get started by creating your first task'}
                  </p>
                  {!state.selectedTodo && (
                    <Button onClick={() => setSelectedTodo(null)}>
                      Create Your First Task
                    </Button>
                  )}
                </div>
              ) : (
                <TodoList
                  todos={filteredTodos}
                  onEdit={handleEditTodo}
                  onDelete={handleDeleteTodo}
                  onUpdate={handleUpdateTodo}
                />
              )}
            </CardContent>
          </Card>
        </motion.section>
      </div>
  );
}