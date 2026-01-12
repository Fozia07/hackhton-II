'use client'

import { useAuth } from '@/contexts/AuthContext'
import { signOut } from '@/lib/auth/client'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export function Header() {
  const { state } = useAuth()
  const { user, isAuthenticated } = state
  const router = useRouter()

  const handleSignOut = async () => {
    try {
      await signOut()
      router.push('/login')
      router.refresh()
    } catch (error) {
      console.error('Sign out error:', error)
    }
  }

  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/dashboard" className="text-xl font-bold text-blue-600">
          Todo App
        </Link>

        {isAuthenticated && user && (
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user.username}</span>
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