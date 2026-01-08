import { cn } from '@/lib/utils'
import * as React from 'react'

interface FormFieldProps {
  label: string
  error?: string
  children: React.ReactNode
  className?: string
}

const FormField = ({ label, error, children, className }: FormFieldProps) => {
  return (
    <div className={cn('mb-4', className)}>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      {children}
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  )
}

interface FormProps extends React.FormHTMLAttributes<HTMLFormElement> {
  children: React.ReactNode
  onSubmit: (e: React.FormEvent) => void
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
  )
}

export { Form, FormField }