import { Form, FormField } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { useCreateTask } from '@/hooks/useCreateTask'

export function CreateTaskForm() {
  const [title, setTitle] = useState('')
  const [error, setError] = useState('')
  const createTaskMutation = useCreateTask()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!title.trim()) {
      setError('Task title is required')
      return
    }

    createTaskMutation.mutate(
      { title: title.trim() },
      {
        onSuccess: () => {
          setTitle('')
          setError('')
        },
        onError: (err) => {
          setError('Failed to create task: ' + err.message)
        },
      }
    )
  }

  return (
    <Form onSubmit={handleSubmit} className="flex gap-2">
      <FormField label="" error={error}>
        <Input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter a new task..."
          disabled={createTaskMutation.isPending}
        />
      </FormField>
      <Button
        type="submit"
        disabled={createTaskMutation.isPending}
        className="mt-6"
      >
        {createTaskMutation.isPending ? 'Adding...' : 'Add Task'}
      </Button>
    </Form>
  )
}