import { useMutation } from '@tanstack/react-query'
import { api } from '@/lib/api/client'

export function useApiMutation<TData, TVariables = void>(
  endpoint: string,
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'POST'
) {
  return useMutation({
    mutationFn: (variables: TVariables) => {
      switch (method) {
        case 'POST':
          return api.post<TData>(endpoint, variables)
        case 'PUT':
          return api.put<TData>(endpoint, variables)
        case 'PATCH':
          return api.patch<TData>(endpoint, variables)
        case 'DELETE':
          return api.delete<TData>(endpoint)
        default:
          throw new Error(`Unsupported method: ${method}`)
      }
    },
  })
}