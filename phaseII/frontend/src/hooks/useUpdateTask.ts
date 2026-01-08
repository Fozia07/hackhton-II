import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api/client'
import { type UpdateTaskInput } from '@/types/task'

export function useUpdateTask(taskId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: Partial<UpdateTaskInput>) => {
      const response = await api.patch(`/api/v1/tasks/${taskId}`, data)
      return response
    },
    onMutate: async (data) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['tasks'] })

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData(['tasks'])

      // Optimistically update
      queryClient.setQueryData(['tasks'], (old: any) =>
        old?.map((task: any) =>
          task.id === taskId ? { ...task, ...data } : task
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