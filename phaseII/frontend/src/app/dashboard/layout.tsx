'use client'

import { useState, useEffect } from 'react'
import { Header } from '@/components/layout/Header'
import { TodoProvider } from '@/contexts/TodoContext'
import { useAuth } from '@/contexts/AuthContext'
import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [mounted, setMounted] = useState(false)
  const { state: authState } = useAuth()
  const reducedMotion = useReducedMotion()

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return null
  }

  return (
    <TodoProvider authState={authState}>
      <motion.div
        initial={reducedMotion ? {} : { opacity: 0 }}
        animate={reducedMotion ? {} : { opacity: 1 }}
        transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        className="min-h-screen bg-gradient-to-br from-background via-primary-50/20 to-secondary-50/10 dark:from-background dark:via-primary-900/5 dark:to-secondary-900/5"
      >
        <Header />
        <main className="container mx-auto py-8 px-4">
          {children}
        </main>
      </motion.div>
    </TodoProvider>
  )
}