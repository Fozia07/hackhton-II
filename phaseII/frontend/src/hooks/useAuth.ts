import { useSession } from '@/lib/auth/client'
import { type User } from '@/types/auth'

export function useAuth() {
  const session = useSession()
  const isLoading = session.isLoading

  // Transform Better Auth user to match our User type
  const rawUser = session.user
  const user: User | null = rawUser ? {
    id: rawUser.id,
    email: rawUser.email,
    username: rawUser.username,
    created_at: rawUser.created_at,
    updated_at: rawUser.updated_at,
    is_active: rawUser.is_active
  } : null

  const isAuthenticated = session.isAuthenticated

  return {
    user,
    isAuthenticated,
    isLoading,
    error: session.error,
  }
}