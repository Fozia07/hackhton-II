import { Modal } from '@/components/ui/modal'
import { Form, FormField } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { Task } from '@/types/task'
import { useUpdateTask } from '@/hooks/useUpdateTask'

interface EditTaskModalProps {
  task: Task
  isOpen: boolean
  onClose: () => void
}

export function EditTaskModal({ task, isOpen, onClose }: EditTaskModalProps) {
  const [title, setTitle] = useState(task.title)
  const [error, setError] = useState('')
  const updateTaskMutation = useUpdateTask(task.id)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!title.trim()) {
      setError('Task title is required')
      return
    }

    updateTaskMutation.mutate(
      { title: title.trim() },
      {
        onSuccess: () => {
          onClose()
        },
        onError: (err) => {
          setError('Failed to update task: ' + err.message)
        },
      }
    )
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Edit Task"
      className="max-w-md"
    >
      <Form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm">
            {error}
          </div>
        )}

        <FormField label="Task Title" error="">
          <Input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Update task title..."
            disabled={updateTaskMutation.isPending}
          />
        </FormField>

        <div className="flex justify-end space-x-2 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={updateTaskMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={updateTaskMutation.isPending}
          >
            {updateTaskMutation.isPending ? 'Saving...' : 'Save'}
          </Button>
        </div>
      </Form>
    </Modal>
  )
}