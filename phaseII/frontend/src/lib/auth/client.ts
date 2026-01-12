import authService from './service';
import { useState, useEffect } from 'react';
import { User, Session, SignupData, SigninData } from '../../types/auth';

// Custom authentication methods using our JWT service
export const signIn = {
  email: async ({ email, password }: { email: string; password: string }) => {
    // For our backend, we use username instead of email for signin
    // So we'll pass the email as the username to the signin method
    const data: SigninData = {
      username: email,
      password,
    };

    const result = await authService.signin(data);
    if (result.error) {
      return { error: { message: result.error.message } };
    }

    return { data: result.data };
  },
};

export const signUp = {
  email: async ({ email, password, name }: { email: string; password: string; name: string }) => {
    // Our backend uses username instead of name, so we'll use the name as username
    const data: SignupData = {
      username: name,
      email,
      password,
    };

    const result = await authService.signup(data);
    if (result.error) {
      return { error: { message: result.error.message } };
    }

    return { data: result.data };
  },
};

export const signOut = async () => {
  await authService.logout();
  return {};
};

// Custom hook for session management
export const useSession = () => {
  const [session, setSession] = useState<Session>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    const fetchSession = async () => {
      setSession(prev => ({ ...prev, isLoading: true }));

      try {
        // Check if user is authenticated by checking token
        const isAuthenticated = authService.isAuthenticated();

        if (!isAuthenticated) {
          setSession({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
          return;
        }

        // If authenticated, fetch user details
        const result = await authService.getCurrentUser();
        if (result.error) {
          // If getting user fails, logout and clear session
          await authService.logout();
          setSession({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: new Error(result.error.message),
          });
          return;
        }

        setSession({
          user: result.data as User,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      } catch (error: any) {
        setSession({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: error instanceof Error ? error : new Error('Unknown error'),
        });
      }
    };

    fetchSession();

    // Listen for storage changes to handle logout from other tabs
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'auth_token' && !e.newValue) {
        setSession({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  return session;
};