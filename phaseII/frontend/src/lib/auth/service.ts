// src/lib/auth/service.ts
import type { User as UserType, AuthResponse, SignupData, SigninData } from '../../types/auth';

interface ApiResponse<T> {
  data?: T;
  error?: {
    message: string;
    status?: number;
  };
}

class AuthService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
  }

  /**
   * Signs up a new user
   */
  async signup(data: SignupData): Promise<ApiResponse<UserType>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          error: {
            message: errorData.detail || `Signup failed with status ${response.status}`,
            status: response.status,
          },
        };
      }

      const userData: UserType = await response.json();
      return { data: userData };
    } catch (error: any) {
      return {
        error: {
          message: error.message || 'Network error occurred during signup',
        },
      };
    }
  }

  /**
   * Signs in an existing user
   */
  async signin(data: SigninData): Promise<ApiResponse<AuthResponse>> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          error: {
            message: errorData.detail || `Signin failed with status ${response.status}`,
            status: response.status,
          },
        };
      }

      const authData: AuthResponse = await response.json();
      // Store the token in localStorage
      this.setToken(authData.access_token);
      return { data: authData };
    } catch (error: any) {
      return {
        error: {
          message: error.message || 'Network error occurred during signin',
        },
      };
    }
  }

  /**
   * Logs out the current user
   */
  async logout(): Promise<void> {
    this.removeToken();
  }

  /**
   * Gets the current user using the stored token
   */
  async getCurrentUser(): Promise<ApiResponse<UserType>> {
    const token = this.getToken();
    if (!token) {
      return {
        error: {
          message: 'No token found',
        },
      };
    }

    try {
      const response = await fetch(`${this.baseUrl}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token might be expired, remove it
          this.removeToken();
        }
        const errorData = await response.json().catch(() => ({}));
        return {
          error: {
            message: errorData.detail || `Failed to get user with status ${response.status}`,
            status: response.status,
          },
        };
      }

      const userData: UserType = await response.json();
      return { data: userData };
    } catch (error: any) {
      return {
        error: {
          message: error.message || 'Network error occurred while fetching user data',
        },
      };
    }
  }

  /**
   * Gets the stored JWT token
   */
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  /**
   * Sets the JWT token in storage
   */
  setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  /**
   * Removes the JWT token from storage
   */
  removeToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  /**
   * Checks if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    // Check if token is expired by decoding the JWT payload
    try {
      // Split the token to get the payload part (second part)
      const parts = token.split('.');
      if (parts.length !== 3) {
        return false; // Invalid JWT format
      }

      // Decode the payload (second part)
      const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
      const currentTime = Math.floor(Date.now() / 1000);

      // Check if token is expired (with a small buffer to account for clock differences)
      const isExpired = payload.exp <= (currentTime + 60); // 1 minute buffer

      if (isExpired) {
        // Remove expired token
        this.removeToken();
        return false;
      }

      return true;
    } catch (error) {
      // If we can't decode the token, assume it's invalid
      console.error('Error decoding JWT token:', error);
      return false;
    }
  }

  /**
   * Refreshes the JWT token
   */
  async refreshToken(): Promise<ApiResponse<string>> {
    // For this implementation, we'll return an error since the backend doesn't have a refresh endpoint
    // In a real implementation, you'd need a refresh token endpoint on the backend
    return {
      error: {
        message: 'Refresh token endpoint not implemented in backend',
      },
    };
  }
}

// Create a singleton instance of the AuthService
const authService = new AuthService();

export default authService;