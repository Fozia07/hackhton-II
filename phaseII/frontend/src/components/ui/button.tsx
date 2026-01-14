// Enhanced Button Component with Soft Colors and Obvious Hover Effects
'use client';

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-60 ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-primary-600 text-white shadow-[var(--shadow-sm)] hover:bg-primary-700 hover:shadow-[var(--shadow-md)] active:bg-primary-800 active:shadow-[var(--shadow-sm)]',
        destructive: 'bg-error-600 text-white shadow-[var(--shadow-sm)] hover:bg-error-700 hover:shadow-[var(--shadow-md)] active:bg-error-800 active:shadow-[var(--shadow-sm)]',
        outline: 'border-2 border-neutral-300 bg-transparent text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-800 hover:border-neutral-400 dark:hover:border-neutral-600 hover:shadow-[var(--shadow-sm)] active:bg-neutral-100 dark:active:bg-neutral-700',
        secondary: 'bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 border border-neutral-200 dark:border-neutral-700 shadow-[var(--shadow-sm)] hover:bg-neutral-200 dark:hover:bg-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600 hover:shadow-[var(--shadow-md)] active:bg-neutral-300 dark:active:bg-neutral-600',
        ghost: 'bg-transparent text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 hover:shadow-[var(--shadow-sm)] active:bg-neutral-200 dark:active:bg-neutral-700',
        link: 'text-primary-600 dark:text-primary-500 underline-offset-4 hover:underline hover:text-primary-700 dark:hover:text-primary-400',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3 text-xs',
        lg: 'h-11 rounded-md px-8 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  animate?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, animate = true, asChild, ...props }, ref) => {
    const reducedMotion = useReducedMotion();
    const buttonClasses = cn(buttonVariants({ variant, size, className }));

    // Multi-signal hover effects: scale + shadow (shadow handled by CSS)
    const hoverAnimation = reducedMotion ? {} : { scale: 1.05 };
    const tapAnimation = reducedMotion ? {} : { scale: 0.98 };

    // Use motion.button only when animations are enabled
    if (animate && !reducedMotion) {
      return (
        <motion.button
          whileHover={hoverAnimation}
          whileTap={tapAnimation}
          transition={{ duration: 0.2, ease: 'easeOut' }}
          className={buttonClasses}
          ref={ref}
          {...(props as any)}
        />
      );
    }

    // Default button without animations
    return (
      <button
        className={buttonClasses}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
