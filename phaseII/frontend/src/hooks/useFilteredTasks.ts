import { useMemo } from 'react'
import { useTasks } from './useTasks'
import { useTaskFilter } from './useTaskFilter'

export function useFilteredTasks() {
  const tasksQuery = useTasks()
  const { filter, searchQuery } = useTaskFilter()

  const filteredTasks = useMemo(() => {
    if (!tasksQuery.data) return []

    let filtered = tasksQuery.data

    // Apply filter
    if (filter === 'active') {
      filtered = filtered.filter(task => !task.completed)
    } else if (filter === 'completed') {
      filtered = filtered.filter(task => task.completed)
    }

    // Apply search
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(query)
      )
    }

    return filtered
  }, [tasksQuery.data, filter, searchQuery])

  return {
    data: filteredTasks,
    isLoading: tasksQuery.isLoading,
    isError: tasksQuery.isError,
    error: tasksQuery.error,
  }
}