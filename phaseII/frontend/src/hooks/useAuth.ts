import { useSession } from '@/lib/auth/client'
import { type User } from '@/types/auth'

export function useAuth() {
  const sessionQuery = useSession()
  const session = sessionQuery.data
  const isLoading = sessionQuery.isPending

  // Transform Better Auth user to match our User type
  const rawUser = session?.user || null
  const user: User | null = rawUser ? {
    id: rawUser.id,
    email: rawUser.email,
    name: rawUser.name,
    createdAt: rawUser.createdAt instanceof Date ? rawUser.createdAt.toISOString() : rawUser.createdAt
  } : null

  const isAuthenticated = !!session?.user

  return {
    user,
    isAuthenticated,
    isLoading,
    error: sessionQuery.error, // Better Auth handles errors internally
  }
}