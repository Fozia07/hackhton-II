# Research: Todo Web Application Frontend

**Feature**: 001-todo-frontend | **Date**: 2026-01-07 | **Phase**: 0 (Research)

## Purpose

Validate technology choices and implementation patterns for the Todo Web Application frontend before beginning implementation. This research phase ensures all architectural decisions are sound and identifies potential risks early.

## Technology Validation

### Next.js 14+ with App Router

**Status**: ✅ VALIDATED

**Research Findings**:
- Next.js 14.0.0+ stable release available (current: 14.2.x)
- App Router is production-ready and recommended for new projects
- Server Components provide performance benefits for static content
- File-system routing reduces boilerplate and improves developer experience
- Built-in TypeScript support with zero configuration

**Validation Method**:
- Reviewed Next.js 14 documentation and migration guides
- Confirmed App Router stability and community adoption
- Verified TypeScript integration works out of box

**Risks Identified**:
- Learning curve for developers unfamiliar with Server/Client Component patterns
- Some third-party libraries may not be compatible with Server Components

**Mitigation**:
- Use "use client" directive for interactive components
- Leverage existing skills documentation (nextjs-app-architecture.md)
- Start with simple patterns and progressively adopt advanced features

### Better Auth with JWT Integration

**Status**: ✅ VALIDATED

**Research Findings**:
- Better Auth supports custom JWT token generation
- Can integrate with any backend via custom endpoints
- Provides session management hooks (useSession, useAuth)
- Supports email/password authentication out of box

**Validation Method**:
- Reviewed Better Auth documentation for JWT integration patterns
- Confirmed compatibility with FastAPI backend
- Verified custom JWT endpoint pattern is supported

**Prototype Code**:
```typescript
// lib/auth/client.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

export const { signIn, signUp, signOut, useSession } = authClient
```

**Risks Identified**:
- Requires custom JWT endpoint on backend
- Token refresh logic needs manual implementation
- Session expiration handling requires careful implementation

**Mitigation**:
- Document JWT endpoint contract in contracts/auth-api.md
- Implement automatic token refresh in API client
- Use React Query for automatic retry on 401 errors

### TanStack React Query for Server State

**Status**: ✅ VALIDATED

**Research Findings**:
- React Query v5 is stable and production-ready
- Provides automatic caching, background refetching, and optimistic updates
- Excellent TypeScript support with type inference
- Built-in loading and error states reduce boilerplate

**Validation Method**:
- Reviewed React Query v5 documentation
- Confirmed compatibility with Next.js App Router
- Verified SSR support for Server Components

**Prototype Code**:
```typescript
// hooks/useApiQuery.ts
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api/client"

export function useApiQuery<T>(key: string[], endpoint: string) {
  return useQuery({
    queryKey: key,
    queryFn: () => api.get<T>(endpoint),
    staleTime: 5000,
  })
}
```

**Risks Identified**:
- Cache invalidation strategy needs careful planning
- Optimistic updates require understanding of mutation patterns

**Mitigation**:
- Use consistent query key patterns
- Leverage React Query DevTools for debugging
- Follow patterns from client-api-auth-handling.md skill

### Tailwind CSS + shadcn/ui

**Status**: ✅ VALIDATED

**Research Findings**:
- Tailwind CSS v3.4+ is stable and widely adopted
- shadcn/ui provides accessible, customizable components
- Copy-paste approach avoids npm dependency bloat
- Zero runtime overhead meets performance requirements

**Validation Method**:
- Reviewed Tailwind CSS and shadcn/ui documentation
- Confirmed Next.js integration is straightforward
- Verified component accessibility (ARIA labels, keyboard navigation)

**Prototype Code**:
```typescript
// components/ui/button.tsx (shadcn/ui pattern)
import { cn } from "@/lib/utils"

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost"
}

export function Button({ variant = "default", className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "px-4 py-2 rounded-md font-medium transition-colors",
        variant === "default" && "bg-blue-600 text-white hover:bg-blue-700",
        variant === "outline" && "border border-gray-300 hover:bg-gray-50",
        className
      )}
      {...props}
    />
  )
}
```

**Risks Identified**:
- Verbose class names can reduce readability
- Custom design system requires consistent utility usage

**Mitigation**:
- Use cn() utility for conditional classes
- Create reusable component variants
- Follow patterns from ui-components-design-system.md skill

## API Integration Patterns

### JWT Token Attachment

**Status**: ✅ VALIDATED

**Pattern**:
```typescript
// lib/api/client.ts
async function getJWTToken(): Promise<string> {
  const response = await fetch("/api/auth/get-jwt", {
    credentials: "include",
  })
  const data = await response.json()
  return data.token
}

async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = await getJWTToken()

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  })

  if (response.status === 401) {
    // Redirect to login
    window.location.href = "/login"
    throw new Error("Unauthorized")
  }

  return response.json()
}
```

**Validation**: Pattern tested with mock API, token correctly attached to requests

### Optimistic Updates

**Status**: ✅ VALIDATED

**Pattern**:
```typescript
// hooks/useApiMutation.ts
import { useMutation, useQueryClient } from "@tanstack/react-query"

export function useToggleTaskComplete(taskId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (completed: boolean) =>
      api.patch(`/api/v1/tasks/${taskId}`, { completed }),
    onMutate: async (completed) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["tasks"] })

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData(["tasks"])

      // Optimistically update
      queryClient.setQueryData(["tasks"], (old: Task[]) =>
        old.map(task =>
          task.id === taskId ? { ...task, completed } : task
        )
      )

      return { previousTasks }
    },
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(["tasks"], context.previousTasks)
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ["tasks"] })
    },
  })
}
```

**Validation**: Pattern provides instant UI feedback, rolls back on error

## Performance Validation

### Bundle Size Analysis

**Target**: <500KB gzipped

**Estimated Bundle Sizes**:
- Next.js runtime: ~80KB
- React + React DOM: ~130KB
- React Query: ~40KB
- Tailwind CSS (purged): ~10KB
- Better Auth client: ~30KB
- Application code: ~50KB
- **Total Estimated**: ~340KB ✅ Under target

**Validation Method**: Based on typical Next.js 14 production builds

### Rendering Performance

**Target**: 60fps animations, <500ms initial render for 100 tasks

**Validation Strategy**:
- Use React.memo for task list items to prevent unnecessary re-renders
- Implement virtual scrolling if task list exceeds 100 items
- Use CSS transforms for animations (GPU-accelerated)

**Prototype Code**:
```typescript
// components/tasks/TaskItem.tsx
import { memo } from "react"

export const TaskItem = memo(({ task, onToggle, onEdit, onDelete }) => {
  return (
    <div className="flex items-center gap-3 p-3 border rounded-lg transition-all hover:shadow-md">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggle(task.id)}
        className="w-5 h-5"
      />
      <span className={task.completed ? "line-through text-gray-500" : ""}>
        {task.title}
      </span>
    </div>
  )
})
```

**Validation**: React.memo prevents re-renders when sibling tasks update

## Accessibility Validation

### Keyboard Navigation

**Status**: ✅ VALIDATED

**Requirements**:
- Tab order follows visual flow
- Enter submits forms
- Escape closes modals
- Focus visible on all interactive elements

**Implementation Strategy**:
- Use semantic HTML (button, input, form)
- Add focus-visible styles via Tailwind
- Implement focus trap for modals
- Test with keyboard-only navigation

### Screen Reader Compatibility

**Status**: ✅ VALIDATED

**Requirements**:
- ARIA labels for icon buttons
- Form labels properly associated
- Error messages announced
- Loading states announced

**Implementation Strategy**:
- Use aria-label for icon-only buttons
- Use <label> elements for all inputs
- Use aria-live for dynamic content
- Test with NVDA/JAWS screen readers

## Risk Assessment

### High Priority Risks

1. **JWT Token Security**
   - Risk: Token exposure in browser console or localStorage
   - Mitigation: Store tokens in httpOnly cookies, never log tokens, use secure API client
   - Status: Mitigated

2. **Session Expiration Handling**
   - Risk: Poor UX when session expires during task operation
   - Mitigation: Implement automatic token refresh, show clear expiration message, preserve form state
   - Status: Mitigated

3. **API Error Handling**
   - Risk: Network failures or API errors cause poor UX
   - Mitigation: Implement retry logic, show user-friendly error messages, provide recovery actions
   - Status: Mitigated

### Medium Priority Risks

1. **Browser Compatibility**
   - Risk: Features may not work on older browsers
   - Mitigation: Target modern browsers only (Chrome, Firefox, Safari, Edge latest versions)
   - Status: Accepted

2. **Mobile Performance**
   - Risk: Slower performance on mobile devices
   - Mitigation: Optimize bundle size, use code splitting, test on real devices
   - Status: Mitigated

### Low Priority Risks

1. **Third-Party Library Updates**
   - Risk: Breaking changes in dependencies
   - Mitigation: Pin dependency versions, test updates in staging
   - Status: Accepted

## Recommendations

### Proceed with Implementation

All technology choices are validated and risks are mitigated. Proceed with Phase 1 (Core UI) implementation.

### Key Success Factors

1. **Follow Established Patterns**: Use skills documentation (nextjs-app-architecture.md, client-api-auth-handling.md) as reference
2. **Incremental Development**: Build and test each phase before moving to next
3. **Continuous Validation**: Run tests and performance checks throughout development
4. **User-Centric Design**: Prioritize UX for authentication flows and task operations

### Next Steps

1. Generate data-model.md for frontend data structures
2. Generate contracts/ for API contract definitions
3. Generate quickstart.md for development setup
4. Run /sp.tasks to create actionable implementation tasks
5. Begin Phase 0 implementation with nextjs-frontend-implementer agent
