import { useTaskFilter } from '@/hooks/useTaskFilter'
import { Button } from '@/components/ui/button'

export function TaskFilter() {
  const { filter, setFilter } = useTaskFilter()

  return (
    <div className="flex space-x-2">
      <Button
        variant={filter === 'all' ? 'default' : 'outline'}
        onClick={() => setFilter('all')}
      >
        All
      </Button>
      <Button
        variant={filter === 'active' ? 'default' : 'outline'}
        onClick={() => setFilter('active')}
      >
        Active
      </Button>
      <Button
        variant={filter === 'completed' ? 'default' : 'outline'}
        onClick={() => setFilter('completed')}
      >
        Completed
      </Button>
    </div>
  )
}