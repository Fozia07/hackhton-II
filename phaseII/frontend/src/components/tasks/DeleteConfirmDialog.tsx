import { Modal } from '@/components/ui/modal'
import { Button } from '@/components/ui/button'

interface DeleteConfirmDialogProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  taskTitle: string
}

export function DeleteConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  taskTitle
}: DeleteConfirmDialogProps) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Confirm Deletion"
      className="max-w-md"
    >
      <div className="space-y-4">
        <p>
          Are you sure you want to delete the task "<strong>{taskTitle}</strong>"?
        </p>
        <p className="text-sm text-gray-500">
          This action cannot be undone.
        </p>

        <div className="flex justify-end space-x-2 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="destructive"
            onClick={() => {
              onConfirm()
              onClose()
            }}
          >
            Delete
          </Button>
        </div>
      </div>
    </Modal>
  )
}