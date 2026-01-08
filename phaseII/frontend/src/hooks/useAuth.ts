import { useSession } from '@/lib/auth/client'
import { User } from '@/types/auth'

export function useAuth() {
  const { data: session, isLoading } = useSession()

  const user: User | null = session?.user || null
  const isAuthenticated = !!session?.user

  return {
    user,
    isAuthenticated,
    isLoading,
    error: null, // Better Auth handles errors internally
  }
}