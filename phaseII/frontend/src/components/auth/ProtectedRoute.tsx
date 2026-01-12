'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter, usePathname } from 'next/navigation'
import { type ReactNode, useEffect, useState } from 'react'

interface ProtectedRouteProps {
  children: ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { state } = useAuth()
  const { isAuthenticated, isLoading } = state
  const router = useRouter()
  const pathname = usePathname()

  // Add a client-side check to ensure we're running on the client
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (isClient && !isLoading && !isAuthenticated && pathname !== '/login' && pathname !== '/signup') {
      // Redirect to login if not authenticated and auth check is complete
      router.replace('/login')
    }
  }, [isAuthenticated, isLoading, router, pathname, isClient])

  // Don't render anything on the server or while determining if we're on the client
  if (!isClient) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  // Show loading while checking authentication status
  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Checking authentication...</div>
  }

  // Only render children if authenticated
  if (!isAuthenticated) {
    // Return a placeholder while redirect happens
    return <div className="min-h-screen flex items-center justify-center">Redirecting...</div>
  }

  return <>{children}</>
}