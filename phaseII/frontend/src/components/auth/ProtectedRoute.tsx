'use client'

import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { type ReactNode, useEffect } from 'react'

interface ProtectedRouteProps {
  children: ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Redirect to login if not authenticated
      router.push('/login')
    }
  }, [isAuthenticated, isLoading, router])

  // Show nothing while checking authentication status
  if (isLoading || (!isAuthenticated && !isLoading)) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  // Render children only if authenticated
  return <>{children}</>
}