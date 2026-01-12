'use client'

import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'

export function Navigation() {
  const { state } = useAuth()
  const { isAuthenticated } = state

  return (
    <nav className="bg-gray-800 text-white">
      <div className="container mx-auto px-4 py-3">
        <ul className="flex space-x-6">
          <li>
            <Link href="/" className="hover:text-gray-300">
              Home
            </Link>
          </li>
          {isAuthenticated && (
            <>
              <li>
                <Link href="/dashboard" className="hover:text-gray-300">
                  Dashboard
                </Link>
              </li>
            </>
          )}
          {!isAuthenticated && (
            <>
              <li>
                <Link href="/login" className="hover:text-gray-300">
                  Login
                </Link>
              </li>
              <li>
                <Link href="/signup" className="hover:text-gray-300">
                  Sign Up
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  )
}