import { useTaskFilter } from '@/hooks/useTaskFilter'
import { Input } from '@/components/ui/input'

export function TaskSearch() {
  const { searchQuery, setSearchQuery } = useTaskFilter()

  return (
    <div className="flex-1">
      <Input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search tasks..."
        className="w-full"
      />
    </div>
  )
}