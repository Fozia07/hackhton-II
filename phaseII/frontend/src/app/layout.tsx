import './globals.css'
import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import { ReactQueryClientProvider } from '@/components/providers/ReactQueryClientProvider'
import { TaskFilterProvider } from '@/contexts/TaskFilterContext'
import { AuthProviderWrapper } from '@/components/providers/AuthProviderWrapper'
import { ThemeProvider } from '@/contexts/ThemeProvider'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'Todo App - Modern Task Management',
  description: 'A beautiful and professional todo application with soft colors and gentle animations',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: 'hsl(0, 0%, 100%)' },
    { media: '(prefers-color-scheme: dark)', color: 'hsl(210, 18%, 12%)' }
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="light" suppressHydrationWarning>
      <body className={`${inter.className} antialiased transition-colors duration-300 ease-in-out`}>
        <ThemeProvider>
          <ReactQueryClientProvider>
            <AuthProviderWrapper>
              <div className="min-h-screen transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)]">
                {children}
              </div>
            </AuthProviderWrapper>
          </ReactQueryClientProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}