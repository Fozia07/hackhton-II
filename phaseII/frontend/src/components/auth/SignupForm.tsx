'use client'

import { Form, FormField } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import { signUp } from '@/lib/auth/client'
import { useRouter } from 'next/navigation'

export function SignupForm() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    try {
      const result = await signUp.email({
        email,
        password,
        name,
      })

      if (result?.error) {
        setError(result.error?.message || 'Signup failed')
      } else {
        // Redirect to dashboard on successful signup
        router.push('/dashboard')
        router.refresh()
      }
    } catch (err) {
      setError('An error occurred during signup')
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

      <FormField label="Full Name" error="">
        <Input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="John Doe"
          required
        />
      </FormField>

      <FormField label="Email" error="">
        <Input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="your@email.com"
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

      <FormField label="Confirm Password" error="">
        <Input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="••••••••"
          required
        />
      </FormField>

      <Button
        type="submit"
        className="w-full mt-4"
        disabled={loading}
      >
        {loading ? 'Creating account...' : 'Create account'}
      </Button>
    </Form>
  )
}