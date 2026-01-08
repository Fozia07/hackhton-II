/**
 * Test file to verify Better Auth client exports work correctly
 * This file demonstrates the proper way to import and use Better Auth functions
 */

// Import individual functions (this should now work without TypeScript errors)
import { signIn, signUp, signOut, useSession } from './client'

// Verify that the functions can be called properly
const testImports = () => {
  // These should not produce TypeScript errors anymore
  console.log('signIn function:', typeof signIn)
  console.log('signUp function:', typeof signUp)
  console.log('signOut function:', typeof signOut)
  console.log('useSession function:', typeof useSession)
}

export { testImports }

// Example usage patterns that should work:
/*
// In a React component:
import { signIn } from '@/lib/auth/client'
import { useSession } from '@/lib/auth/client'

const MyComponent = () => {
  const { data: session, isLoading } = useSession()

  const handleLogin = async () => {
    const result = await signIn('credentials', {
      email: 'test@example.com',
      password: 'password'
    })
  }
}
*/