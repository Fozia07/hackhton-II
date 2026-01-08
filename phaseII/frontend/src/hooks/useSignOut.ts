import { signOut } from '@/lib/auth/client'
import { useRouter } from 'next/navigation'
import { useMutation } from '@tanstack/react-query'

export function useSignOut() {
  const router = useRouter()

  return useMutation({
    mutationFn: async () => {
      await signOut()
    },
    onSuccess: () => {
      // Redirect to home page on successful logout
      router.push('/')
      router.refresh()
    },
  })
}