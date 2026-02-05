// Checkbox Component with Soft Colors
'use client';

import { cn } from '@/lib/utils';
import * as React from 'react';

export interface CheckboxProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  onCheckedChange?: (checked: boolean) => void;
}

const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, onCheckedChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      // Call the original onChange if provided
      if (props.onChange) {
        props.onChange(e);
      }
      // Call onCheckedChange with the checked value
      if (onCheckedChange) {
        onCheckedChange(e.target.checked);
      }
    };

    return (
      <input
        type="checkbox"
        className={cn(
          'h-5 w-5 rounded border-2 border-neutral-300 dark:border-neutral-600 bg-card transition-all duration-200',
          'hover:border-neutral-400 dark:hover:border-neutral-500',
          'checked:bg-primary-600 checked:border-primary-600 dark:checked:bg-primary-500 dark:checked:border-primary-500',
          'focus:ring-2 focus:ring-primary-400/20 focus:ring-offset-2 focus:outline-none',
          'disabled:cursor-not-allowed disabled:opacity-60 disabled:bg-neutral-100 dark:disabled:bg-neutral-800',
          'cursor-pointer',
          className
        )}
        ref={ref}
        onChange={handleChange}
        {...props}
      />
    );
  }
);
Checkbox.displayName = 'Checkbox';

export { Checkbox };