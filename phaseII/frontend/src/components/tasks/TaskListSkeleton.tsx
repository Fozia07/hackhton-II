export function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {[...Array(5)].map((_, index) => (
        <div
          key={index}
          className="flex items-center gap-3 p-4 border rounded-lg animate-pulse"
        >
          <div className="h-5 w-5 rounded bg-gray-200"></div>
          <div className="flex-1 h-5 rounded bg-gray-200"></div>
          <div className="h-8 w-16 rounded bg-gray-200"></div>
          <div className="h-8 w-16 rounded bg-gray-200"></div>
        </div>
      ))}
    </div>
  )
}