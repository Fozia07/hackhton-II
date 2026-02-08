'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface AuthContextType {
  token: string | null;
  username: string | null;
  isAuthenticated: boolean;
  login: (token: string, username: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenValue] = useState<string | null>(null);
  const [username, setUsernameValue] = useState<string | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Initialize from localStorage on mount
    const savedToken = localStorage.getItem('jwtToken');
    const savedUsername = localStorage.getItem('username');

    if (savedToken && savedUsername) {
      setTokenValue(savedToken);
      setUsernameValue(savedUsername);
    }

    setIsInitialized(true);
  }, []);

  useEffect(() => {
    // Redirect based on authentication state and route
    if (!isInitialized) return;

    const isLoginPage = pathname === '/login';
    const isChatPage = pathname === '/chat' || pathname.startsWith('/chat');

    if (!token && !isLoginPage) {
      // Redirect to login if not authenticated and not on login page
      router.push('/login');
    } else if (token && isLoginPage) {
      // Redirect to chat if authenticated and on login page
      router.push('/chat');
    }
  }, [token, pathname, isInitialized, router]);

  const login = (token: string, username: string) => {
    localStorage.setItem('jwtToken', token);
    localStorage.setItem('username', username);
    setTokenValue(token);
    setUsernameValue(username);
  };

  const logout = () => {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('username');
    setTokenValue(null);
    setUsernameValue(null);
    router.push('/login');
  };

  const value = {
    token,
    username,
    isAuthenticated: !!token && !!username,
    login,
    logout,
  };

  if (!isInitialized) {
    return null; // Render nothing until initialization is complete
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}