import { type Task } from '@/types/task'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { useToggleTaskComplete } from '@/hooks/useToggleTaskComplete'
import { useDeleteTask } from '@/hooks/useDeleteTask'
import { useState } from 'react'
import { EditTaskModal } from './EditTaskModal'

interface TaskItemProps {
  task: Task
}

export function TaskItem({ task }: TaskItemProps) {
  const [showEditModal, setShowEditModal] = useState(false)
  const toggleCompleteMutation = useToggleTaskComplete(task.id)
  const deleteTaskMutation = useDeleteTask()

  const handleToggleComplete = () => {
    toggleCompleteMutation.mutate(!task.completed)
  }

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      deleteTaskMutation.mutate(task.id)
    }
  }

  return (
    <div className={`flex items-center gap-3 p-4 border rounded-lg transition-all hover:shadow-md ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <Checkbox
        checked={task.completed}
        onChange={handleToggleComplete}
        disabled={toggleCompleteMutation.isPending || deleteTaskMutation.isPending}
      />

      <span className={`flex-1 ${task.completed ? 'line-through text-gray-500' : ''}`}>
        {task.title}
      </span>

      <Button
        variant="outline"
        size="sm"
        onClick={() => setShowEditModal(true)}
        disabled={toggleCompleteMutation.isPending || deleteTaskMutation.isPending}
      >
        Edit
      </Button>

      <Button
        variant="destructive"
        size="sm"
        onClick={handleDelete}
        disabled={toggleCompleteMutation.isPending || deleteTaskMutation.isPending}
      >
        Delete
      </Button>

      {showEditModal && (
        <EditTaskModal
          task={task}
          isOpen={showEditModal}
          onClose={() => setShowEditModal(false)}
        />
      )}
    </div>
  )
}