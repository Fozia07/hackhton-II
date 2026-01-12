'use client'

import { Form, FormField } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { signIn } from '@/lib/auth/client'
import { useRouter } from 'next/navigation'

export function LoginForm() {
  const router = useRouter()
  const [username, setUsername] = useState('') // Can be username or email
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const result = await signIn.email({
        email: username, // Our client maps email to username for backend
        password,
      })

      if (result?.error) {
        setError(result.error?.message || 'Login failed')
      } else {
        // Redirect to dashboard on successful login
        router.push('/dashboard')
        router.refresh()
      }
    } catch (err) {
      setError('An error occurred during login')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Form onSubmit={handleSubmit}>
      {error && (
        <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
          {error}
        </div>
      )}

      <FormField label="Username or Email" error="">
        <Input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="username or email"
          required
        />
      </FormField>

      <FormField label="Password" error="">
        <Input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          required
        />
      </FormField>

      <Button
        type="submit"
        className="w-full mt-4"
        disabled={loading}
      >
        {loading ? 'Signing in...' : 'Sign in'}
      </Button>
    </Form>
  )
}