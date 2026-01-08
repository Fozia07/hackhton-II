---
id: 014
title: Create UI Components Design System Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["ui-components", "design-system", "skill-creation", "tailwind", "shadcn-ui", "nextjs"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/ui-components-design-system.md
tests:
  - none (documentation work)
---

## Prompt

create a skill for UI Components, Styling & Design System Skill.

STACK:
- Tailwind CSS
- shadcn/ui

RESPONSIBILITIES:
- Build reusable UI components
- Use shadcn/ui for: Button, Input, Card, Dialog, Form, etc.
- Extend shadcn components (do not rewrite)
- Ensure responsive, mobile-first design
- Maintain consistent spacing, colors, typography
- Apply accessibility best practices

RULES:
- No routing logic
- No API calls
- No authentication logic
- No backend assumptions

## Response snapshot

Created comprehensive UI Components, Styling & Design System skill documentation (28K) at `.claude/skills/ui-components-design-system.md`.

The skill covers:

**shadcn/ui Setup:**
- Installation and initialization
- Configuration (components.json)
- Adding components (button, input, card, dialog, form)

**Using shadcn/ui Components:**
1. Button - variants (default, destructive, outline, secondary, ghost, link), with icons, loading states
2. Input - basic input, with labels, error states
3. Card - CardHeader, CardTitle, CardDescription, CardContent, CardFooter
4. Dialog - DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription
5. Form - with react-hook-form and zod validation, FormField, FormItem, FormLabel, FormControl, FormMessage

**Extending shadcn/ui:**
- Custom button variants (success, warning)
- Custom sizes (xl)
- Using class-variance-authority (cva)

**Responsive Design Patterns:**
- Mobile-first approach with Tailwind breakpoints
- Responsive cards, grids, navigation
- Breakpoint utilities (sm, md, lg, xl)

**Design Tokens:**
- Tailwind configuration with custom colors, spacing, border radius
- CSS variables for theming
- Dark mode support with CSS variables

**Layout Components:**
- Container - responsive container with padding
- Stack - vertical layout with spacing variants
- Grid - responsive grid with cols and gap variants

**Common UI Patterns:**
- Empty state with icon and CTA
- Loading state with spinner
- Error state with alert and retry
- Success state with alert

**Accessibility Best Practices:**
- ARIA labels for icon buttons
- Keyboard navigation support
- Focus management with useRef
- Screen reader support with sr-only and aria-live

**Dark Mode Support:**
- ThemeProvider setup with next-themes
- ThemeToggle component with sun/moon icons
- CSS variables for light/dark themes

**Animation Patterns:**
- Fade in animations
- Slide in animations
- Hover effects with transitions

**Best Practices:**
- Component composition over monolithic components
- Mobile-first responsive design
- Accessibility compliance
- Consistent spacing with Tailwind scale
- Semantic HTML

The skill provides complete UI component patterns with shadcn/ui and Tailwind CSS for building accessible, responsive Next.js applications.

## Outcome

- ✅ Impact: Created production-ready UI Components & Design System skill with comprehensive shadcn/ui patterns, Tailwind CSS utilities, responsive design, accessibility, and dark mode support
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/ui-components-design-system.md (28K)
- 🔁 Next prompts: User may request additional frontend skills (data fetching, state management, forms), implement UI components, or move to other project areas
- 🧠 Reflection: This skill complements the nextjs-app-architecture.md skill by providing the UI layer. Combined with jwt-better-auth-integration.md and the FastAPI skills, developers now have a complete full-stack toolkit for building Next.js + FastAPI applications with proper UI components, routing, authentication, and backend APIs.

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempt to use skill-orchestrator agent was too slow (646K+ tokens), switched to direct creation which was much faster
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): For future skills, create directly instead of using skill-orchestrator agent
