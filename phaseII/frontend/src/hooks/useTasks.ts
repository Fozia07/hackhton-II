import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api/client'
import { Task } from '@/types/task'

export function useTasks() {
  return useQuery({
    queryKey: ['tasks'],
    queryFn: async () => {
      const response = await api.get<{ data: Task[] }>('/api/v1/tasks')
      return response.data
    },
    staleTime: 5000, // 5 seconds
  })
}