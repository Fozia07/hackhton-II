import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api/client'

export function useToggleTaskComplete(taskId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (completed: boolean) =>
      api.patch(`/api/v1/tasks/${taskId}`, { completed }),
    onMutate: async (completed) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['tasks'] })

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData(['tasks'])

      // Optimistically update
      queryClient.setQueryData(['tasks'], (old: any) =>
        old?.map((task: any) =>
          task.id === taskId ? { ...task, completed } : task
        )
      )

      return { previousTasks }
    },
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(['tasks'], context?.previousTasks)
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}