# UI Components, Styling & Design System

## Expertise
Expert skill for building reusable UI components with Tailwind CSS and shadcn/ui. Specializes in component composition, responsive design, accessibility, and maintaining consistent design systems in Next.js applications.

## Purpose
This skill handles UI component development and design systems, enabling you to:
- Build reusable UI components with shadcn/ui
- Extend shadcn components with custom variants
- Implement responsive, mobile-first designs
- Maintain consistent spacing, colors, and typography
- Apply accessibility best practices
- Create component composition patterns
- Handle UI states (loading, error, empty, success)

## When to Use
Use this skill when you need to:
- Set up shadcn/ui in a Next.js project
- Create reusable UI components
- Extend shadcn/ui components
- Implement responsive layouts
- Apply consistent design tokens
- Ensure accessibility compliance
- Build form components with validation UI
- Create common UI patterns

## Core Concepts

### shadcn/ui Philosophy

shadcn/ui is NOT a component library - it's a collection of reusable components that you copy into your project and own. This means:
- Components live in your codebase (`components/ui/`)
- You can modify them freely
- No package dependencies to manage
- Full control over styling and behavior

### Installation and Setup

**Install Dependencies**:
```bash
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge
npm install @radix-ui/react-slot
npm install lucide-react
```

**Initialize shadcn/ui**:
```bash
npx shadcn-ui@latest init
```

**Configuration** (`components.json`):
```json
{
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

**Add Components**:
```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add form
```

## Using shadcn/ui Components

### 1. Button Component

**Basic Usage**:
```tsx
import { Button } from "@/components/ui/button";

export function ButtonDemo() {
  return (
    <div className="flex gap-4">
      <Button>Default</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  );
}
```

**With Icons**:
```tsx
import { Button } from "@/components/ui/button";
import { Mail } from "lucide-react";

export function ButtonWithIcon() {
  return (
    <Button>
      <Mail className="mr-2 h-4 w-4" />
      Login with Email
    </Button>
  );
}
```

**Loading State**:
```tsx
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export function ButtonLoading() {
  return (
    <Button disabled>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Please wait
    </Button>
  );
}
```

### 2. Input Component

**Basic Input**:
```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function InputDemo() {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Label htmlFor="email">Email</Label>
      <Input type="email" id="email" placeholder="Email" />
    </div>
  );
}
```

**Input with Error State**:
```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function InputWithError() {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Label htmlFor="email">Email</Label>
      <Input
        type="email"
        id="email"
        placeholder="Email"
        className="border-red-500"
      />
      <p className="text-sm text-red-500">Invalid email address</p>
    </div>
  );
}
```

### 3. Card Component

**Basic Card**:
```tsx
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function CardDemo() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
        <CardDescription>Card Description</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Card Content</p>
      </CardContent>
      <CardFooter>
        <Button>Action</Button>
      </CardFooter>
    </Card>
  );
}
```

### 4. Dialog Component

**Basic Dialog**:
```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

export function DialogDemo() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
}
```

### 5. Form Component

**Form with Validation**:
```tsx
"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const formSchema = z.object({
  username: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
  email: z.string().email({
    message: "Please enter a valid email address.",
  }),
});

export function ProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>
                This is your public display name.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="email@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
```

## Extending shadcn/ui Components

### Custom Button Variants

**Extend Button** (`components/ui/button.tsx`):
```tsx
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "underline-offset-4 hover:underline text-primary",
        // Custom variants
        success: "bg-green-600 text-white hover:bg-green-700",
        warning: "bg-yellow-600 text-white hover:bg-yellow-700",
      },
      size: {
        default: "h-10 py-2 px-4",
        sm: "h-9 px-3 rounded-md",
        lg: "h-11 px-8 rounded-md",
        icon: "h-10 w-10",
        // Custom size
        xl: "h-14 px-10 text-lg rounded-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
```

**Usage**:
```tsx
<Button variant="success">Success</Button>
<Button variant="warning" size="xl">Warning</Button>
```

## Responsive Design Patterns

### Mobile-First Approach

```tsx
export function ResponsiveCard() {
  return (
    <Card className="w-full sm:w-96 md:w-[500px] lg:w-[600px]">
      <CardHeader>
        <CardTitle className="text-lg sm:text-xl md:text-2xl">
          Responsive Title
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div>Item 1</div>
          <div>Item 2</div>
          <div>Item 3</div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Responsive Grid

```tsx
export function ResponsiveGrid() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {items.map((item) => (
        <Card key={item.id}>
          <CardContent>{item.name}</CardContent>
        </Card>
      ))}
    </div>
  );
}
```

### Responsive Navigation

```tsx
export function ResponsiveNav() {
  return (
    <nav className="flex flex-col sm:flex-row gap-2 sm:gap-4">
      <Button variant="ghost" className="w-full sm:w-auto">
        Home
      </Button>
      <Button variant="ghost" className="w-full sm:w-auto">
        About
      </Button>
      <Button variant="ghost" className="w-full sm:w-auto">
        Contact
      </Button>
    </nav>
  );
}
```

## Design Tokens

### Tailwind Configuration

**tailwind.config.ts**:
```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      spacing: {
        "18": "4.5rem",
        "88": "22rem",
        "128": "32rem",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

### CSS Variables

**app/globals.css**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}
```

## Layout Components

### Container

```tsx
import { cn } from "@/lib/utils";

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
}

export function Container({ children, className }: ContainerProps) {
  return (
    <div className={cn("container mx-auto px-4 sm:px-6 lg:px-8", className)}>
      {children}
    </div>
  );
}
```

### Stack (Vertical Layout)

```tsx
import { cn } from "@/lib/utils";

interface StackProps {
  children: React.ReactNode;
  spacing?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

const spacingMap = {
  sm: "space-y-2",
  md: "space-y-4",
  lg: "space-y-6",
  xl: "space-y-8",
};

export function Stack({ children, spacing = "md", className }: StackProps) {
  return (
    <div className={cn("flex flex-col", spacingMap[spacing], className)}>
      {children}
    </div>
  );
}
```

### Grid

```tsx
import { cn } from "@/lib/utils";

interface GridProps {
  children: React.ReactNode;
  cols?: 1 | 2 | 3 | 4 | 6 | 12;
  gap?: "sm" | "md" | "lg";
  className?: string;
}

const colsMap = {
  1: "grid-cols-1",
  2: "grid-cols-1 sm:grid-cols-2",
  3: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3",
  4: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-4",
  6: "grid-cols-2 sm:grid-cols-3 lg:grid-cols-6",
  12: "grid-cols-12",
};

const gapMap = {
  sm: "gap-2",
  md: "gap-4",
  lg: "gap-6",
};

export function Grid({ children, cols = 3, gap = "md", className }: GridProps) {
  return (
    <div className={cn("grid", colsMap[cols], gapMap[gap], className)}>
      {children}
    </div>
  );
}
```

## Common UI Patterns

### Empty State

```tsx
import { FileQuestion } from "lucide-react";
import { Button } from "@/components/ui/button";

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <FileQuestion className="h-12 w-12 text-muted-foreground mb-4" />
      <h3 className="text-lg font-semibold mb-2">No items found</h3>
      <p className="text-sm text-muted-foreground mb-4">
        Get started by creating your first item.
      </p>
      <Button>Create Item</Button>
    </div>
  );
}
```

### Loading State

```tsx
import { Loader2 } from "lucide-react";

export function LoadingState() {
  return (
    <div className="flex items-center justify-center py-12">
      <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
    </div>
  );
}
```

### Error State

```tsx
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export function ErrorState({ error, retry }: { error: string; retry?: () => void }) {
  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>Error</AlertTitle>
      <AlertDescription className="flex items-center justify-between">
        <span>{error}</span>
        {retry && (
          <Button variant="outline" size="sm" onClick={retry}>
            Try Again
          </Button>
        )}
      </AlertDescription>
    </Alert>
  );
}
```

### Success State

```tsx
import { CheckCircle2 } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export function SuccessState({ message }: { message: string }) {
  return (
    <Alert className="border-green-500 bg-green-50 text-green-900">
      <CheckCircle2 className="h-4 w-4 text-green-600" />
      <AlertTitle>Success</AlertTitle>
      <AlertDescription>{message}</AlertDescription>
    </Alert>
  );
}
```

## Accessibility Best Practices

### ARIA Labels

```tsx
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

export function AccessibleButton() {
  return (
    <Button
      variant="ghost"
      size="icon"
      aria-label="Close dialog"
    >
      <X className="h-4 w-4" />
    </Button>
  );
}
```

### Keyboard Navigation

```tsx
"use client";

import { Button } from "@/components/ui/button";

export function KeyboardNav() {
  return (
    <div
      role="navigation"
      aria-label="Main navigation"
      onKeyDown={(e) => {
        if (e.key === "ArrowRight") {
          // Navigate to next item
        }
        if (e.key === "ArrowLeft") {
          // Navigate to previous item
        }
      }}
    >
      <Button>Home</Button>
      <Button>About</Button>
      <Button>Contact</Button>
    </div>
  );
}
```

### Focus Management

```tsx
"use client";

import { useRef, useEffect } from "react";
import { Input } from "@/components/ui/input";

export function FocusManagement() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Auto-focus on mount
    inputRef.current?.focus();
  }, []);

  return (
    <Input
      ref={inputRef}
      placeholder="Auto-focused input"
      className="focus:ring-2 focus:ring-primary focus:ring-offset-2"
    />
  );
}
```

### Screen Reader Support

```tsx
export function ScreenReaderText() {
  return (
    <div>
      <span className="sr-only">Loading...</span>
      <div aria-live="polite" aria-atomic="true">
        <p>Content loaded successfully</p>
      </div>
    </div>
  );
}
```

## Dark Mode Support

### Theme Provider

```tsx
"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { type ThemeProviderProps } from "next-themes/dist/types";

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
```

### Theme Toggle

```tsx
"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

## Animation Patterns

### Fade In

```tsx
export function FadeIn({ children }: { children: React.ReactNode }) {
  return (
    <div className="animate-in fade-in duration-500">
      {children}
    </div>
  );
}
```

### Slide In

```tsx
export function SlideIn({ children }: { children: React.ReactNode }) {
  return (
    <div className="animate-in slide-in-from-bottom duration-500">
      {children}
    </div>
  );
}
```

### Hover Effects

```tsx
import { Card } from "@/components/ui/card";

export function HoverCard() {
  return (
    <Card className="transition-all hover:shadow-lg hover:-translate-y-1">
      <CardContent>Hover me!</CardContent>
    </Card>
  );
}
```

## Best Practices

### 1. Component Composition
```tsx
// ✅ Good - Compose components
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>

// ❌ Bad - Monolithic component
<CustomCard title="Title" content="Content" />
```

### 2. Responsive Design
```tsx
// ✅ Good - Mobile-first
<div className="w-full sm:w-96 md:w-[500px]">

// ❌ Bad - Desktop-first
<div className="w-[500px] md:w-96 sm:w-full">
```

### 3. Accessibility
```tsx
// ✅ Good - Accessible
<Button aria-label="Close">
  <X className="h-4 w-4" />
</Button>

// ❌ Bad - Not accessible
<Button>
  <X className="h-4 w-4" />
</Button>
```

### 4. Consistent Spacing
```tsx
// ✅ Good - Tailwind spacing scale
<div className="space-y-4">
  <div className="p-4">Item 1</div>
  <div className="p-4">Item 2</div>
</div>

// ❌ Bad - Arbitrary values
<div style={{ marginBottom: "17px" }}>
```

## Summary

This skill provides comprehensive guidance for building UI components with Tailwind CSS and shadcn/ui:

**Core Capabilities:**
- shadcn/ui setup and component usage
- Extending components with custom variants
- Responsive, mobile-first design patterns
- Design tokens and theming
- Layout components (Container, Stack, Grid)

**UI Patterns:**
- Empty, loading, error, and success states
- Form components with validation UI
- Accessible components with ARIA labels
- Dark mode support
- Animation and transitions

**Best Practices:**
- Component composition over monolithic components
- Mobile-first responsive design
- Accessibility compliance (ARIA, keyboard navigation, focus management)
- Consistent spacing and typography
- Semantic HTML and screen reader support

Use this skill to build consistent, accessible, and responsive UI components in your Next.js applications with Tailwind CSS and shadcn/ui.
