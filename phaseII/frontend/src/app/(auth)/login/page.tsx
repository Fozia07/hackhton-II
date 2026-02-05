'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { LoginForm } from '@/components/auth/LoginForm';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

export default function LoginPage() {
  const reducedMotion = useReducedMotion();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background to-primary-100/30 dark:from-background dark:to-primary-900/10 py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
        animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
        transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-md"
      >
        <Card className="backdrop-blur-sm bg-card/95 shadow-[var(--shadow-lg)]">
          <CardHeader>
            <CardTitle className="text-2xl text-center text-foreground">Sign in to your account</CardTitle>
            <CardDescription className="text-center text-muted-foreground">
              Enter your credentials to access your todo list
            </CardDescription>
          </CardHeader>
          <CardContent>
            <LoginForm />
            <div className="mt-6 text-center text-sm text-muted-foreground">
              Don't have an account?{' '}
              <Link href="/signup" className="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors duration-200">
                Sign up
              </Link>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}