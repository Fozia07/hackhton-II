// src/hooks/useAuthOperations.ts
'use client';

import { useState } from 'react';
import { signIn as authSignIn, signUp as authSignUp, signOut as authSignOut } from '@/lib/auth/client';

export const useAuthOperations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const signIn = async (credentials: { email: string; password: string }) => {
    setLoading(true);
    setError(null);
    try {
      const result = await authSignIn.email(credentials);
      return result;
    } catch (err: any) {
      setError(err.message || 'Sign in failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const signUp = async (credentials: { email: string; password: string; name?: string }) => {
    setLoading(true);
    setError(null);
    try {
      const result = await authSignUp.email(credentials);
      return result;
    } catch (err: any) {
      setError(err.message || 'Sign up failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const signOutUser = async () => {
    setLoading(true);
    setError(null);
    try {
      await authSignOut();
    } catch (err: any) {
      setError(err.message || 'Sign out failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    signIn,
    signUp,
    signOut: signOutUser,
    loading,
    error,
  };
};