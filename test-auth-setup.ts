// test-auth-setup.ts - This is just a test file to validate the setup
import { signIn, signUp, signOut, useSession } from '@/lib/auth/client';
import { useAuth } from '@/contexts/AuthContext';
import { useAuthOperations } from '@/hooks/useAuthOperations';

console.log('Auth client functions imported successfully');

// This would be used in a component
const exampleUsage = () => {
  // useSession is a hook
  // const session = useSession();

  // useAuth comes from context
  // const { user, isAuthenticated } = useAuth();

  // useAuthOperations provides wrapped functions with loading/error states
  // const { signIn, signUp, signOut, loading, error } = useAuthOperations();

  return 'Setup validated';
};

export default exampleUsage;