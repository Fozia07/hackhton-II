'use client'

import { Header } from '@/components/layout/Header'
import { TodoProvider } from '@/contexts/TodoContext'
import { useAuth } from '@/contexts/AuthContext'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { state: authState } = useAuth()

  return (
    <TodoProvider authState={authState}>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto py-8 px-4">
          {children}
        </main>
      </div>
    </TodoProvider>
  )
}