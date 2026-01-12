import React, { createContext, useContext, useReducer, useEffect } from 'react';
import authService from '../lib/auth/service';
import { User } from '../types/auth';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthAction {
  type: string;
  payload?: any;
}

interface AuthContextType {
  state: AuthState;
  login: (username: string, password: string) => Promise<void>;
  signup: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  getCurrentUser: () => Promise<void>;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOADING':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'AUTH_ERROR':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    // Check if user is authenticated on initial load
    const checkAuthStatus = async () => {
      dispatch({ type: 'LOADING' });

      try {
        const isAuthenticated = authService.isAuthenticated();

        if (isAuthenticated) {
          // Get current user details
          const result = await authService.getCurrentUser();

          if (result.data) {
            dispatch({ type: 'SET_USER', payload: result.data });
          } else {
            // Token exists but is invalid/expired
            await authService.logout();
            dispatch({ type: 'LOGOUT' });
          }
        } else {
          dispatch({ type: 'LOGOUT' });
        }
      } catch (error: any) {
        console.error('Authentication check error:', error);
        dispatch({
          type: 'AUTH_ERROR',
          payload: error.message || 'Failed to check authentication status'
        });
      } finally {
        // Ensure loading state is cleared even if there's an error
        // We don't need to dispatch anything here since the appropriate state
        // has already been set by the success or failure cases above
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (username: string, password: string) => {
    dispatch({ type: 'LOADING' });

    try {
      const result = await authService.signin({
        username,
        password,
      });

      if (result.error) {
        dispatch({ type: 'AUTH_ERROR', payload: result.error.message });
        throw new Error(result.error.message);
      }

      // Get user details after successful login
      const userResult = await authService.getCurrentUser();

      if (userResult.data) {
        dispatch({ type: 'SET_USER', payload: userResult.data });
      } else {
        dispatch({ type: 'AUTH_ERROR', payload: 'Failed to get user data after login' });
        throw new Error('Failed to get user data after login');
      }
    } catch (error: any) {
      dispatch({
        type: 'AUTH_ERROR',
        payload: error.message || 'Login failed'
      });
      throw error;
    } finally {
      // Ensure loading state is handled appropriately
    }
  };

  const signup = async (username: string, email: string, password: string) => {
    dispatch({ type: 'LOADING' });

    try {
      const result = await authService.signup({
        username,
        email,
        password,
      });

      if (result.error) {
        dispatch({ type: 'AUTH_ERROR', payload: result.error.message });
        throw new Error(result.error.message);
      }

      // Auto-login after successful signup
      await login(username, password);
    } catch (error: any) {
      dispatch({
        type: 'AUTH_ERROR',
        payload: error.message || 'Signup failed'
      });
      throw error;
    } finally {
      // Ensure loading state is handled appropriately
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      dispatch({ type: 'LOGOUT' });
    } catch (error: any) {
      console.error('Logout error:', error);
      dispatch({
        type: 'LOGOUT' // Still proceed with logout state even if service fails
      });
    }
  };

  const getCurrentUser = async () => {
    try {
      const result = await authService.getCurrentUser();

      if (result.data) {
        dispatch({ type: 'SET_USER', payload: result.data });
        return result.data;
      } else {
        dispatch({ type: 'AUTH_ERROR', payload: result.error?.message || 'Failed to get user' });
        return null;
      }
    } catch (error: any) {
      dispatch({
        type: 'AUTH_ERROR',
        payload: error.message || 'Failed to get user'
      });
      return null;
    }
  };

  const value = {
    state,
    login,
    signup,
    logout,
    getCurrentUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};