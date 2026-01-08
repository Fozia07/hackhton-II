# Client Logic, API Integration & Auth Handling

## Expertise
Expert skill for implementing client-side authentication, API integration, and state management in Next.js applications using Better Auth and JWT-secured FastAPI backends. Specializes in auth flows, session management, API client patterns, and error handling.

## Purpose
This skill handles frontend authentication and API integration, enabling you to:
- Integrate Better Auth client in Next.js
- Implement signup, signin, and logout flows
- Manage authenticated user state
- Attach JWT tokens to API requests automatically
- Centralize API client logic
- Handle loading, error, and success states
- Implement auth-protected routes
- Manage token refresh and expiration

## When to Use
Use this skill when you need to:
- Set up Better Auth client
- Implement authentication flows
- Create API client with JWT attachment
- Manage user session state
- Handle authentication errors
- Implement protected routes
- Create auth-aware React hooks
- Handle API request states

## Core Concepts

### Authentication Flow

```
1. User visits app
   ↓
2. Check session with Better Auth
   ↓
3. If authenticated:
   - Get JWT token
   - Attach to API requests
   - Access protected resources
   ↓
4. If not authenticated:
   - Redirect to login
   - User signs in
   - Better Auth creates session
   - Get JWT token
   - Redirect to app
```

## Better Auth Client Setup

### 1. Install Dependencies

```bash
npm install better-auth
npm install @tanstack/react-query  # For data fetching
```

### 2. Create Auth Client

**lib/auth-client.ts**:
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

// Export auth methods
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  getSession,
} = authClient;
```

### 3. Environment Variables

**.env.local**:
```bash
# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Authentication Flows

### 1. Sign Up Flow

**hooks/use-signup.ts**:
```typescript
"use client";

import { useState } from "react";
import { signUp } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

interface SignUpData {
  email: string;
  password: string;
  name?: string;
}

export function useSignUp() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const signup = async (data: SignUpData) => {
    setLoading(true);
    setError(null);

    try {
      const result = await signUp.email({
        email: data.email,
        password: data.password,
        name: data.name,
      });

      if (result.error) {
        setError(result.error.message);
        return { success: false, error: result.error.message };
      }

      // Redirect to dashboard after successful signup
      router.push("/dashboard");
      return { success: true };
    } catch (err) {
      const message = err instanceof Error ? err.message : "Signup failed";
      setError(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  };

  return { signup, loading, error };
}
```

**Usage in Component**:
```typescript
"use client";

import { useSignUp } from "@/hooks/use-signup";

export function SignUpForm() {
  const { signup, loading, error } = useSignUp();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const result = await signup({
      email: formData.get("email") as string,
      password: formData.get("password") as string,
      name: formData.get("name") as string,
    });

    if (result.success) {
      console.log("Signup successful!");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" placeholder="Name" />
      <input name="email" type="email" placeholder="Email" />
      <input name="password" type="password" placeholder="Password" />
      {error && <p>{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? "Signing up..." : "Sign Up"}
      </button>
    </form>
  );
}
```

### 2. Sign In Flow

**hooks/use-signin.ts**:
```typescript
"use client";

import { useState } from "react";
import { signIn } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

interface SignInData {
  email: string;
  password: string;
}

export function useSignIn() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const signin = async (data: SignInData) => {
    setLoading(true);
    setError(null);

    try {
      const result = await signIn.email({
        email: data.email,
        password: data.password,
      });

      if (result.error) {
        setError(result.error.message);
        return { success: false, error: result.error.message };
      }

      // Redirect to dashboard after successful signin
      router.push("/dashboard");
      return { success: true };
    } catch (err) {
      const message = err instanceof Error ? err.message : "Sign in failed";
      setError(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  };

  return { signin, loading, error };
}
```

### 3. Sign Out Flow

**hooks/use-signout.ts**:
```typescript
"use client";

import { useState } from "react";
import { signOut } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export function useSignOut() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const logout = async () => {
    setLoading(true);

    try {
      await signOut();
      router.push("/login");
    } catch (err) {
      console.error("Sign out failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return { logout, loading };
}
```

## Session Management

### 1. useSession Hook

**hooks/use-auth.ts**:
```typescript
"use client";

import { useSession } from "@/lib/auth-client";

export function useAuth() {
  const { data: session, isPending, error } = useSession();

  return {
    user: session?.user ?? null,
    session: session?.session ?? null,
    isAuthenticated: !!session?.user,
    isLoading: isPending,
    error,
  };
}
```

**Usage**:
```typescript
"use client";

import { useAuth } from "@/hooks/use-auth";

export function UserProfile() {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <div>Please sign in</div>;
  }

  return (
    <div>
      <h2>Welcome, {user.name}</h2>
      <p>Email: {user.email}</p>
    </div>
  );
}
```

### 2. Protected Route Component

**components/protected-route.tsx**:
```typescript
"use client";

import { useAuth } from "@/hooks/use-auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

export function ProtectedRoute({
  children,
  redirectTo = "/login",
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectTo);
    }
  }, [isAuthenticated, isLoading, router, redirectTo]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
```

**Usage**:
```typescript
// app/dashboard/page.tsx
import { ProtectedRoute } from "@/components/protected-route";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div>Dashboard Content</div>
    </ProtectedRoute>
  );
}
```

## API Client with JWT

### 1. API Client Setup

**lib/api-client.ts**:
```typescript
import { getSession } from "@/lib/auth-client";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Get JWT token from Better Auth session.
 */
async function getJWTToken(): Promise<string | null> {
  try {
    const session = await getSession();

    if (!session?.data?.session) {
      return null;
    }

    // Get JWT token from Better Auth
    const response = await fetch("/api/auth/get-jwt", {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data.token;
  } catch (error) {
    console.error("Failed to get JWT token:", error);
    return null;
  }
}

/**
 * API request options.
 */
interface ApiRequestOptions extends RequestInit {
  requiresAuth?: boolean;
}

/**
 * Fetch wrapper that automatically attaches JWT token.
 */
export async function apiFetch<T>(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<T> {
  const { requiresAuth = true, ...fetchOptions } = options;

  // Prepare headers
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...fetchOptions.headers,
  };

  // Attach JWT token if authentication is required
  if (requiresAuth) {
    const token = await getJWTToken();

    if (!token) {
      throw new Error("Authentication required");
    }

    headers["Authorization"] = `Bearer ${token}`;
  }

  // Make request
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  // Handle errors
  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: "Request failed",
    }));

    if (response.status === 401) {
      // Redirect to login on authentication error
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
      throw new Error("Authentication required");
    }

    if (response.status === 403) {
      throw new Error("Access denied");
    }

    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

/**
 * API client methods.
 */
export const api = {
  get: <T>(endpoint: string, options?: ApiRequestOptions) =>
    apiFetch<T>(endpoint, { ...options, method: "GET" }),

  post: <T>(endpoint: string, data?: any, options?: ApiRequestOptions) =>
    apiFetch<T>(endpoint, {
      ...options,
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    }),

  put: <T>(endpoint: string, data?: any, options?: ApiRequestOptions) =>
    apiFetch<T>(endpoint, {
      ...options,
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    }),

  patch: <T>(endpoint: string, data?: any, options?: ApiRequestOptions) =>
    apiFetch<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: data ? JSON.stringify(data) : undefined,
    }),

  delete: <T>(endpoint: string, options?: ApiRequestOptions) =>
    apiFetch<T>(endpoint, { ...options, method: "DELETE" }),
};
```

### 2. JWT Token Endpoint

**app/api/auth/get-jwt/route.ts**:
```typescript
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    // Get session from Better Auth
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session?.user) {
      return NextResponse.json(
        { error: "Not authenticated" },
        { status: 401 }
      );
    }

    // Generate JWT token
    const token = await auth.api.signJWT({
      payload: {
        sub: session.user.id,
        email: session.user.email,
      },
    });

    return NextResponse.json({ token });
  } catch (error) {
    console.error("Failed to generate JWT:", error);
    return NextResponse.json(
      { error: "Failed to generate token" },
      { status: 500 }
    );
  }
}
```

## API Request Hooks

### 1. useApiQuery Hook

**hooks/use-api-query.ts**:
```typescript
"use client";

import { useQuery, UseQueryOptions } from "@tanstack/react-query";
import { api } from "@/lib/api-client";

export function useApiQuery<T>(
  key: string[],
  endpoint: string,
  options?: Omit<UseQueryOptions<T>, "queryKey" | "queryFn">
) {
  return useQuery<T>({
    queryKey: key,
    queryFn: () => api.get<T>(endpoint),
    ...options,
  });
}
```

**Usage**:
```typescript
"use client";

import { useApiQuery } from "@/hooks/use-api-query";

interface User {
  id: string;
  email: string;
  name: string;
}

export function UserProfile() {
  const { data: user, isLoading, error } = useApiQuery<User>(
    ["user", "me"],
    "/api/v1/users/me"
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>No user data</div>;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}
```

### 2. useApiMutation Hook

**hooks/use-api-mutation.ts**:
```typescript
"use client";

import { useMutation, UseMutationOptions, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";

interface ApiMutationOptions<TData, TVariables> {
  method: "post" | "put" | "patch" | "delete";
  endpoint: string;
  invalidateKeys?: string[][];
  onSuccess?: (data: TData) => void;
  onError?: (error: Error) => void;
}

export function useApiMutation<TData = any, TVariables = any>(
  options: ApiMutationOptions<TData, TVariables>
) {
  const queryClient = useQueryClient();

  return useMutation<TData, Error, TVariables>({
    mutationFn: (variables: TVariables) => {
      switch (options.method) {
        case "post":
          return api.post<TData>(options.endpoint, variables);
        case "put":
          return api.put<TData>(options.endpoint, variables);
        case "patch":
          return api.patch<TData>(options.endpoint, variables);
        case "delete":
          return api.delete<TData>(options.endpoint);
        default:
          throw new Error(`Unsupported method: ${options.method}`);
      }
    },
    onSuccess: (data) => {
      // Invalidate queries
      if (options.invalidateKeys) {
        options.invalidateKeys.forEach((key) => {
          queryClient.invalidateQueries({ queryKey: key });
        });
      }

      // Call custom onSuccess
      options.onSuccess?.(data);
    },
    onError: options.onError,
  });
}
```

**Usage**:
```typescript
"use client";

import { useApiMutation } from "@/hooks/use-api-mutation";

interface UpdateUserData {
  name: string;
  email: string;
}

export function UpdateProfileForm() {
  const updateUser = useApiMutation<User, UpdateUserData>({
    method: "put",
    endpoint: "/api/v1/users/me",
    invalidateKeys: [["user", "me"]],
    onSuccess: () => {
      console.log("Profile updated!");
    },
    onError: (error) => {
      console.error("Update failed:", error);
    },
  });

  const handleSubmit = (data: UpdateUserData) => {
    updateUser.mutate(data);
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);
      handleSubmit({
        name: formData.get("name") as string,
        email: formData.get("email") as string,
      });
    }}>
      <input name="name" placeholder="Name" />
      <input name="email" type="email" placeholder="Email" />
      {updateUser.error && <p>{updateUser.error.message}</p>}
      <button type="submit" disabled={updateUser.isPending}>
        {updateUser.isPending ? "Updating..." : "Update Profile"}
      </button>
    </form>
  );
}
```

## Error Handling

### 1. API Error Types

**lib/api-errors.ts**:
```typescript
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export class AuthenticationError extends ApiError {
  constructor(message: string = "Authentication required") {
    super(message, 401, "AUTHENTICATION_ERROR");
    this.name = "AuthenticationError";
  }
}

export class AuthorizationError extends ApiError {
  constructor(message: string = "Access denied") {
    super(message, 403, "AUTHORIZATION_ERROR");
    this.name = "AuthorizationError";
  }
}

export class ValidationError extends ApiError {
  constructor(
    message: string,
    public errors?: Record<string, string[]>
  ) {
    super(message, 422, "VALIDATION_ERROR");
    this.name = "ValidationError";
  }
}

export class NotFoundError extends ApiError {
  constructor(message: string = "Resource not found") {
    super(message, 404, "NOT_FOUND_ERROR");
    this.name = "NotFoundError";
  }
}
```

### 2. Error Handler Component

**components/error-boundary.tsx**:
```typescript
"use client";

import { useEffect } from "react";
import { ApiError } from "@/lib/api-errors";

interface ErrorBoundaryProps {
  error: Error;
  reset: () => void;
}

export function ErrorBoundary({ error, reset }: ErrorBoundaryProps) {
  useEffect(() => {
    console.error("Error:", error);
  }, [error]);

  if (error instanceof ApiError) {
    return (
      <div>
        <h2>API Error</h2>
        <p>Status: {error.statusCode}</p>
        <p>Message: {error.message}</p>
        <button onClick={reset}>Try Again</button>
      </div>
    );
  }

  return (
    <div>
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try Again</button>
    </div>
  );
}
```

## Loading States

### 1. Global Loading Provider

**components/loading-provider.tsx**:
```typescript
"use client";

import { createContext, useContext, useState, ReactNode } from "react";

interface LoadingContextType {
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
}

const LoadingContext = createContext<LoadingContextType | undefined>(undefined);

export function LoadingProvider({ children }: { children: ReactNode }) {
  const [isLoading, setLoading] = useState(false);

  return (
    <LoadingContext.Provider value={{ isLoading, setLoading }}>
      {children}
      {isLoading && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white" />
        </div>
      )}
    </LoadingContext.Provider>
  );
}

export function useLoading() {
  const context = useContext(LoadingContext);
  if (!context) {
    throw new Error("useLoading must be used within LoadingProvider");
  }
  return context;
}
```

### 2. Suspense Boundaries

```typescript
import { Suspense } from "react";

export function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<div>Loading user data...</div>}>
        <UserProfile />
      </Suspense>

      <Suspense fallback={<div>Loading posts...</div>}>
        <PostList />
      </Suspense>
    </div>
  );
}
```

## React Query Setup

### 1. Query Client Provider

**app/providers.tsx**:
```typescript
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

**app/layout.tsx**:
```typescript
import { Providers } from "./providers";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Best Practices

### 1. Centralized API Client
```typescript
// ✅ Good - Use centralized API client
import { api } from "@/lib/api-client";
const user = await api.get("/api/v1/users/me");

// ❌ Bad - Direct fetch calls
const response = await fetch("/api/v1/users/me");
```

### 2. Error Handling
```typescript
// ✅ Good - Handle errors properly
try {
  const data = await api.get("/api/v1/users/me");
} catch (error) {
  if (error instanceof AuthenticationError) {
    // Handle auth error
  }
}

// ❌ Bad - Ignore errors
const data = await api.get("/api/v1/users/me");
```

### 3. Loading States
```typescript
// ✅ Good - Show loading state
const { data, isLoading } = useApiQuery(["user"], "/api/v1/users/me");
if (isLoading) return <div>Loading...</div>;

// ❌ Bad - No loading state
const { data } = useApiQuery(["user"], "/api/v1/users/me");
return <div>{data.name}</div>; // Crashes if data is undefined
```

### 4. Token Management
```typescript
// ✅ Good - Automatic token attachment
const data = await api.get("/api/v1/users/me");

// ❌ Bad - Manual token management
const token = await getToken();
const response = await fetch("/api/v1/users/me", {
  headers: { Authorization: `Bearer ${token}` }
});
```

## Summary

This skill provides comprehensive guidance for client-side authentication and API integration:

**Authentication:**
- Better Auth client setup
- Sign up, sign in, sign out flows
- Session management with useSession
- Protected routes and components

**API Integration:**
- Centralized API client with JWT attachment
- Automatic token refresh
- Error handling with custom error types
- Request/response interceptors

**State Management:**
- React Query integration
- useApiQuery and useApiMutation hooks
- Loading and error states
- Query invalidation

**Best Practices:**
- Centralized API client
- Proper error handling
- Loading state management
- Automatic token attachment
- Type-safe API calls

Use this skill to implement robust client-side authentication and API integration in your Next.js applications with Better Auth and JWT-secured FastAPI backends.
