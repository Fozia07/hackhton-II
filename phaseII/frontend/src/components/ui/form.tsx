// Form Component with Gentle Validation Feedback
'use client';

import { cn } from '@/lib/utils';
import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

interface FormFieldProps {
  label: string;
  error?: string;
  success?: string;
  children: React.ReactNode;
  className?: string;
  required?: boolean;
}

const FormField = ({ label, error, success, children, className, required }: FormFieldProps) => {
  const reducedMotion = useReducedMotion();

  return (
    <div className={cn('mb-4', className)}>
      <label className="block text-sm font-medium text-foreground mb-1.5">
        {label}
        {required && <span className="text-error-500 ml-1">*</span>}
      </label>
      {children}
      <AnimatePresence mode="wait">
        {error && (
          <motion.p
            key="error"
            initial={reducedMotion ? {} : { opacity: 0, y: -4 }}
            animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
            exit={reducedMotion ? {} : { opacity: 0, y: -4 }}
            transition={{ duration: 0.2 }}
            className="mt-1.5 text-sm text-error-600 dark:text-error-500"
          >
            {error}
          </motion.p>
        )}
        {success && !error && (
          <motion.p
            key="success"
            initial={reducedMotion ? {} : { opacity: 0, y: -4 }}
            animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
            exit={reducedMotion ? {} : { opacity: 0, y: -4 }}
            transition={{ duration: 0.2 }}
            className="mt-1.5 text-sm text-success-600 dark:text-success-500"
          >
            {success}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
};

interface FormProps extends React.FormHTMLAttributes<HTMLFormElement> {
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent) => void;
}

const Form = ({ children, onSubmit, className, ...props }: FormProps) => {
  return (
    <form
      onSubmit={onSubmit}
      className={cn('space-y-4', className)}
      {...props}
    >
      {children}
    </form>
  );
};

export { Form, FormField };