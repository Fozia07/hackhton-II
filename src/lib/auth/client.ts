// src/lib/auth/client.ts
'use client';

import { createAuthClient } from 'better-auth/react';

// Create the auth client with proper configuration to avoid TypeScript callable errors
const authClient = createAuthClient({
  fetchOptions: {
    // Configure base URL for API calls
    baseURL: process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000',
    // Use 'manual' redirect to avoid fetch API redirect enum error
    redirect: 'manual',
  },
  // Enable/disable specific features
  plugins: [],
});

// Export individual functions separately to avoid TypeScript destructuring issues
// The original approach of destructuring ({ signIn, signUp, ... } = authClient)
// causes TypeScript errors because the resulting object doesn't have proper call signatures
export const signIn = authClient.signIn;
export const signUp = authClient.signUp;
export const signOut = authClient.signOut;
export const useSession = authClient.useSession;
export const getClientUser = authClient.getClientUser;
export const updateClientUser = authClient.updateClientUser;
export const forgotPassword = authClient.forgotPassword;
export const resetPassword = authClient.resetPassword;
export const changePassword = authClient.changePassword;
export const verifyEmail = authClient.verifyEmail;
export const resendVerification = authClient.resendVerification;
export const social = authClient.social;
export const withAuth = authClient.withAuth;

// Export the entire client if direct access is needed
export { authClient };