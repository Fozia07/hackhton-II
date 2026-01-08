import { signUp } from '@/lib/auth/client'
import { useRouter } from 'next/navigation'
import { useMutation } from '@tanstack/react-query'

export function useSignUp() {
  const router = useRouter()

  return useMutation({
    mutationFn: async ({ email, password, name }: { email: string; password: string; name: string }) => {
      const result = await signUp.email({
        email,
        password,
        name,
      })

      if (result?.error) {
        throw new Error(result.error?.message || 'Signup failed')
      }

      return result
    },
    onSuccess: () => {
      // Redirect to dashboard on successful signup
      router.push('/dashboard')
      router.refresh()
    },
  })
}