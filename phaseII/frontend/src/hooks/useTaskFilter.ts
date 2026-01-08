import { useTaskFilter as useTaskFilterContext } from '../contexts/TaskFilterContext'

export function useTaskFilter() {
  return useTaskFilterContext()
}