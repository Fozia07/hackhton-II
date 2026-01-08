# Better Auth Setup Guide

This guide explains how to properly set up Better Auth in your Next.js application.

## Setup

1. Install the required dependencies:
```bash
npm install better-auth @better-fetch/fetch
```

2. Set up your environment variables as shown in `.env.example`

3. The auth client is configured in `src/lib/auth/client.ts` and exports the following functions:
   - `signIn` - Sign in with email/password or social providers
   - `signUp` - Sign up with email/password
   - `signOut` - Sign out the current user
   - `useSession` - Hook to get current session info
   - `social` - Object containing social sign-in methods

## Usage

### In Components

Use the `useAuth` hook to access authentication state:

```tsx
import { useAuth } from '@/contexts/AuthContext';

export default function MyComponent() {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {isAuthenticated ? (
        <p>Welcome {user?.name || user?.email}</p>
      ) : (
        <p>Please sign in</p>
      )}
    </div>
  );
}
```

### Using Auth Operations

Use the `useAuthOperations` hook to perform sign in/out operations:

```tsx
import { useAuthOperations } from '@/hooks/useAuthOperations';

export default function AuthComponent() {
  const { signIn, signUp, signOut, loading, error } = useAuthOperations();

  const handleLogin = async () => {
    try {
      await signIn({ email: 'user@example.com', password: 'password' });
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <div>
      {/* Login form */}
    </div>
  );
}
```

### Protected Routes

Use the `ProtectedRoute` component to protect routes:

```tsx
import ProtectedRoute from '@/components/ProtectedRoute';

export default function ProtectedPage() {
  return (
    <ProtectedRoute>
      <div>This content is protected</div>
    </ProtectedRoute>
  );
}
```

## Configuration

The auth client is configured with proper TypeScript types and handles all the common authentication flows. The setup includes:

- Proper client-side session management
- Error handling
- Loading states
- Type safety

## API Routes

The API route at `/api/auth/[...all]/route.ts` handles all authentication requests and callbacks.