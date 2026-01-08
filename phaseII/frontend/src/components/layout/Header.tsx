'use client'

import { useAuth } from '@/hooks/useAuth'
import { useSignOut } from '@/hooks/useSignOut'
import Link from 'next/link'

export function Header() {
  const { user, isAuthenticated } = useAuth()
  const signOutMutation = useSignOut()

  const handleSignOut = () => {
    signOutMutation.mutate()
  }

  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/dashboard" className="text-xl font-bold text-blue-600">
          Todo App
        </Link>

        {isAuthenticated && user && (
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user.name}</span>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  )
}