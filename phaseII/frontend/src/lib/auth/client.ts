import { createAuthClient } from 'better-auth/react';

// Create the auth client with proper configuration
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  fetchOptions: {
    // Use 'manual' redirect to avoid fetch API redirect enum error
    redirect: 'manual',
  },
});

// Export the auth client methods
// Better Auth has specific method structures
export const signIn = authClient.signIn;
export const signUp = authClient.signUp;
export const signOut = authClient.signOut;
export const useSession = authClient.useSession;