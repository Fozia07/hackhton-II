import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ReactQueryClientProvider } from '@/components/providers/ReactQueryClientProvider'
import { TaskFilterProvider } from '@/contexts/TaskFilterContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ReactQueryClientProvider>
          <TaskFilterProvider>
            {children}
          </TaskFilterProvider>
        </ReactQueryClientProvider>
      </body>
    </html>
  )
}