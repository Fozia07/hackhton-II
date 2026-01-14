'use client';

import { Form, FormField } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { signUp } from '@/lib/auth/client';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

export function SignupForm() {
  const router = useRouter();
  const reducedMotion = useReducedMotion();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    if (!email.includes('@')) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    if (!validateForm()) {
      setLoading(false);
      return;
    }

    try {
      const result = await signUp.email({
        email,
        password,
        name: username, // Backend expects name but uses it as username
      });

      if (result?.error) {
        setErrors({ general: result.error?.message || 'Signup failed' });
      } else {
        // Redirect to dashboard on successful signup
        router.push('/dashboard');
        router.refresh();
      }
    } catch (err) {
      setErrors({ general: 'An error occurred during signup' });
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <AnimatePresence mode="wait">
        {errors.general && (
          <motion.div
            key="error"
            initial={reducedMotion ? {} : { opacity: 0, y: -10 }}
            animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
            exit={reducedMotion ? {} : { opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="mb-4 p-3 bg-error-50 dark:bg-error-900/20 text-error-700 dark:text-error-400 rounded-md text-sm border border-error-200 dark:border-error-800"
          >
            {errors.general}
          </motion.div>
        )}
      </AnimatePresence>

      <FormField label="Username" error={errors.username} required>
        <Input
          type="text"
          value={username}
          onChange={(e) => {
            setUsername(e.target.value);
            if (errors.username) setErrors({ ...errors, username: '' });
          }}
          placeholder="johndoe"
          required
          minLength={3}
          maxLength={150}
          error={!!errors.username}
        />
      </FormField>

      <FormField label="Email" error={errors.email} required>
        <Input
          type="email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            if (errors.email) setErrors({ ...errors, email: '' });
          }}
          placeholder="your@email.com"
          required
          error={!!errors.email}
        />
      </FormField>

      <FormField label="Password" error={errors.password} required>
        <Input
          type="password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            if (errors.password) setErrors({ ...errors, password: '' });
          }}
          placeholder="••••••••"
          required
          minLength={8}
          error={!!errors.password}
        />
      </FormField>

      <FormField label="Confirm Password" error={errors.confirmPassword} required>
        <Input
          type="password"
          value={confirmPassword}
          onChange={(e) => {
            setConfirmPassword(e.target.value);
            if (errors.confirmPassword) setErrors({ ...errors, confirmPassword: '' });
          }}
          placeholder="••••••••"
          required
          error={!!errors.confirmPassword}
        />
      </FormField>

      <Button
        type="submit"
        className="w-full mt-6"
        disabled={loading}
      >
        {loading ? 'Creating account...' : 'Create account'}
      </Button>
    </Form>
  );
}