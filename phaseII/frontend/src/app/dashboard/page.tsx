'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { TodoList } from '@/components/todo/TodoList'
import { TodoForm } from '@/components/todo/TodoForm'
import { useTodo } from '@/contexts/TodoContext'
import type { Todo, TodoCreate, TodoUpdate } from '@/types/todo'

export default function DashboardPage() {
  const { state, createTodo, updateTodo, deleteTodo, setSelectedTodo } = useTodo()

  const handleCreateTodo = async (data: TodoCreate) => {
    await createTodo(data)
  }

  const handleDeleteTodo = async (id: number) => {
    await deleteTodo(id)
  }

  const handleEditTodo = (todo: Todo) => {
    setSelectedTodo(todo)
  }

  const handleUpdateTodo = async (id: number, data: Partial<TodoUpdate>) => {
    await updateTodo(id, data)
  }

  const handleCancelEdit = () => {
    setSelectedTodo(null)
  }

  const filteredTodos = state.selectedTodo ? [state.selectedTodo] : state.todos

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Todos</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{state.todos.length}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Active Todos</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{state.todos.filter(t => !t.completed).length}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Completed Todos</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{state.todos.filter(t => t.completed).length}</p>
          </CardContent>
        </Card>
      </div>

      {state.selectedTodo ? (
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Editing Todo</h2>
          <TodoForm
            initialValues={state.selectedTodo}
            onSubmit={(data) => handleUpdateTodo(state.selectedTodo!.id, data as Partial<TodoUpdate>)}
            onCancel={handleCancelEdit}
            isSubmitting={state.isLoading}
          />
        </div>
      ) : (
        <TodoForm
          onSubmit={(data) => handleCreateTodo(data as TodoCreate)}
          isSubmitting={state.isLoading}
        />
      )}

      {state.isLoading ? (
        <div>Loading todos...</div>
      ) : state.error ? (
        <div className="text-red-500">Error: {state.error}</div>
      ) : (
        <TodoList
          todos={filteredTodos}
          onEdit={handleEditTodo}
          onDelete={handleDeleteTodo}
          onUpdate={handleUpdateTodo}
        />
      )}
    </div>
  )
}