// src/contexts/AuthContext.tsx
'use client';

import React, { createContext, useContext, ReactNode } from 'react';
import { useSession } from '@/lib/auth/client';

interface AuthContextType {
  user: any;
  session: any;
  isLoading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const { data: session, isLoading } = useSession();

  const contextValue: AuthContextType = {
    user: session?.user || null,
    session,
    isLoading,
    isAuthenticated: !!session?.user,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};