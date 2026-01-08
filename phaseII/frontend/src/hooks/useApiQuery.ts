import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api/client'

export function useApiQuery<T>(key: string[], endpoint: string) {
  return useQuery({
    queryKey: key,
    queryFn: () => api.get<T>(endpoint),
    staleTime: 5000,
  })
}