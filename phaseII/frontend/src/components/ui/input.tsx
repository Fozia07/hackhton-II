// Input Component with Soft Focus States
'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border bg-card px-3 py-2 text-sm shadow-[0_0_0_1px_hsl(var(--border))] transition-all duration-200',
          'placeholder:text-muted-foreground',
          'hover:border-neutral-400 dark:hover:border-neutral-600',
          'focus-visible:outline-none focus-visible:border-primary-500 focus-visible:ring-2 focus-visible:ring-primary-400/20 focus-visible:shadow-[0_0_0_1px_hsl(var(--primary))]',
          'disabled:cursor-not-allowed disabled:opacity-60 disabled:bg-neutral-50 dark:disabled:bg-neutral-900',
          'file:border-0 file:bg-transparent file:text-sm file:font-medium',
          error && 'border-error-500 focus-visible:border-error-500 focus-visible:ring-error-400/20',
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Input.displayName = 'Input';

export { Input };
