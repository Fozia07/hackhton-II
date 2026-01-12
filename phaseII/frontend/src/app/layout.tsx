import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ReactQueryClientProvider } from '@/components/providers/ReactQueryClientProvider'
import { TaskFilterProvider } from '@/contexts/TaskFilterContext'
import { AuthProviderWrapper } from '@/components/providers/AuthProviderWrapper'

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
          <AuthProviderWrapper>
            {children}
          </AuthProviderWrapper>
        </ReactQueryClientProvider>
      </body>
    </html>
  )
}