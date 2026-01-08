'use client'

import { TaskList } from '@/components/tasks/TaskList'
import { CreateTaskForm } from '@/components/tasks/CreateTaskForm'
import { TaskFilter } from '@/components/tasks/TaskFilter'
import { TaskSearch } from '@/components/tasks/TaskSearch'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useTaskFilter } from '@/hooks/useTaskFilter'
import { useFilteredTasks } from '@/hooks/useFilteredTasks'

export default function DashboardPage() {
  const { filter, searchQuery } = useTaskFilter()
  const { data: tasks = [], isLoading } = useFilteredTasks()

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{tasks.length}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Active Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{tasks.filter(t => !t.completed).length}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Completed Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{tasks.filter(t => t.completed).length}</p>
          </CardContent>
        </Card>
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <TaskFilter />
        <TaskSearch />
      </div>

      <CreateTaskForm />

      {isLoading ? (
        <div>Loading tasks...</div>
      ) : (
        <TaskList tasks={tasks} />
      )}
    </div>
  )
}