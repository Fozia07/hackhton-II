import { signIn } from '@/lib/auth/client'
import { useRouter } from 'next/navigation'
import { useMutation } from '@tanstack/react-query'

export function useSignIn() {
  const router = useRouter()

  return useMutation({
    mutationFn: async ({ email, password }: { email: string; password: string }) => {
      const result = await signIn.email({
        email,
        password,
      })

      if (result?.error) {
        throw new Error(result.error?.message || 'Login failed')
      }

      return result
    },
    onSuccess: () => {
      // Redirect to dashboard on successful login
      router.push('/dashboard')
      router.refresh()
    },
  })
}