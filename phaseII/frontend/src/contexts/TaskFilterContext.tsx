'use client'

import { createContext, useContext, ReactNode, useState } from 'react'
import { TaskFilter } from '@/types/task'

interface TaskFilterContextValue {
  filter: TaskFilter
  setFilter: (filter: TaskFilter) => void
  searchQuery: string
  setSearchQuery: (query: string) => void
}

const TaskFilterContext = createContext<TaskFilterContextValue | null>(null)

interface TaskFilterProviderProps {
  children: ReactNode
}

export function TaskFilterProvider({ children }: TaskFilterProviderProps) {
  const [filter, setFilter] = useState<TaskFilter>('all')
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <TaskFilterContext.Provider value={{
      filter,
      setFilter,
      searchQuery,
      setSearchQuery,
    }}>
      {children}
    </TaskFilterContext.Provider>
  )
}

export function useTaskFilter() {
  const context = useContext(TaskFilterContext)
  if (!context) {
    throw new Error('useTaskFilter must be used within TaskFilterProvider')
  }
  return context
}