# Implementation Plan: Todo Web Application Frontend

**Branch**: `001-todo-frontend` | **Date**: 2026-01-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-frontend/spec.md`

**Note**: This plan covers frontend implementation only. Backend APIs, database models, and infrastructure are out of scope.

## Summary

Build a responsive, authenticated web frontend for a multi-user Todo application using Next.js 14+ App Router, React, TypeScript, and Tailwind CSS. The frontend will communicate with a JWT-secured FastAPI backend via REST API, implementing user authentication (signup/login/logout), task CRUD operations (create, read, update, delete), task completion tracking, and filtering/search capabilities. The implementation follows a spec-driven approach with clear phases: authentication setup, task management UI, and advanced features.

## Technical Context

**Language/Version**: TypeScript 5.x, JavaScript ES2022+
**Primary Dependencies**: Next.js 14+, React 18+, Better Auth, TanStack React Query, Tailwind CSS, shadcn/ui
**Storage**: Browser session storage (JWT tokens), React Query cache (API data)
**Testing**: Jest, React Testing Library, Playwright (E2E)
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge), iOS Safari, Android Chrome
**Project Type**: Web application (frontend only)
**Performance Goals**: <3s page load, <2s task operations, 60fps animations, responsive on mobile/tablet/desktop
**Constraints**: <200ms UI response time, works offline with cached data, accessible (keyboard navigation), secure (no token exposure)
**Scale/Scope**: 5-7 pages/routes, 15-20 React components, 100+ tasks per user, mobile-first responsive design

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Spec-Driven Development**: Implementation follows written specification in `spec.md` with 5 prioritized user stories and 27 functional requirements
✅ **Incremental Evolution**: Frontend is Phase II of the project (Phase I console app completed). This phase remains independently functional
✅ **AI-Native Design**: Uses Claude Code as primary implementation assistant, follows agent-driven development workflow
✅ **Code Quality and Documentation**: Will use TypeScript for type safety, modular component structure, clear API contracts
✅ **Architecture-First Approach**: Clear separation of concerns (UI components, API client, auth logic, state management)
✅ **Container-First Deployment**: Frontend will be containerized (Docker) for deployment alongside backend services

**Constitution Alignment**: ✅ PASS - All principles satisfied for frontend scope

## Agent-Based Workflow

### Frontend Development Approach

This frontend implementation will follow an agent-based workflow:

- **Dedicated Frontend Sub-Agent**: A specialized `nextjs-frontend-implementer` agent will be responsible for all frontend implementation work, including building UI components, implementing pages and layouts, integrating authentication flows, and connecting to backend APIs.

- **Reusable Frontend Skills**: The implementation will leverage conceptually the following skills documented in `.claude/skills/`:
  - `nextjs-app-architecture.md` - Next.js App Router structure, routing patterns, server/client component separation
  - `ui-components-design-system.md` - Tailwind CSS patterns, shadcn/ui component integration, responsive design
  - `client-api-auth-handling.md` - Better Auth integration, JWT token management, API client patterns, React Query hooks
  - `jwt-better-auth-integration.md` - Authentication flow between Next.js frontend and JWT-secured FastAPI backend

- **Directory Structure**: All frontend code will be developed inside a `/frontend` directory within the Phase 2 repository, maintaining clear separation from backend code.

- **Scope Exclusion**: Internal agent wiring, `.claude` configuration details, and agent orchestration mechanics are excluded from this plan. This plan focuses solely on the frontend architecture and implementation strategy.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-frontend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - technology research and validation
├── data-model.md        # Phase 1 output - frontend data structures and state shape
├── quickstart.md        # Phase 1 output - setup and development guide
├── contracts/           # Phase 1 output - API contract definitions
│   ├── auth-api.md      # Authentication endpoints contract
│   └── tasks-api.md     # Task management endpoints contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/            # Auth route group
│   │   │   ├── login/         # Login page
│   │   │   └── signup/        # Signup page
│   │   ├── (dashboard)/       # Protected route group
│   │   │   ├── layout.tsx     # Dashboard layout with auth check
│   │   │   └── page.tsx       # Main dashboard (task list)
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Landing page
│   ├── components/            # React components
│   │   ├── ui/               # shadcn/ui components
│   │   ├── auth/             # Auth-related components
│   │   ├── tasks/            # Task-related components
│   │   └── layout/           # Layout components (header, nav)
│   ├── lib/                  # Utilities and configurations
│   │   ├── auth/             # Better Auth client setup
│   │   ├── api/              # API client with JWT handling
│   │   └── utils/            # Helper functions
│   ├── hooks/                # Custom React hooks
│   │   ├── useAuth.ts        # Authentication hook
│   │   ├── useApiQuery.ts    # API query hook
│   │   └── useApiMutation.ts # API mutation hook
│   ├── types/                # TypeScript type definitions
│   │   ├── auth.ts           # Auth types
│   │   └── task.ts           # Task types
│   └── styles/               # Global styles
│       └── globals.css       # Tailwind CSS imports
├── public/                   # Static assets
├── tests/                    # Test files
│   ├── unit/                # Component unit tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # Playwright E2E tests
├── .env.local               # Environment variables (gitignored)
├── .env.example             # Environment variables template
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
├── package.json             # Dependencies
└── README.md                # Frontend documentation
```

**Structure Decision**: Web application structure (Option 2) selected. Frontend code is isolated in `/frontend` directory with Next.js App Router architecture. This structure supports:
- Clear separation between frontend and backend codebases
- Next.js 14+ App Router conventions (app directory, route groups, layouts)
- Component-based architecture with reusable UI components
- Type-safe API integration with TypeScript
- Test organization by type (unit, integration, E2E)

## Decisions Needing Documentation

### Decision 1: Framework Choice - Next.js with App Router

**Options Considered**:
1. **Next.js 14+ with App Router** (Chosen)
2. Create React App (CRA)
3. Vite + React Router
4. Remix

**Tradeoffs**:
- **Next.js App Router**: Server/client component separation, built-in routing, excellent DX, React Server Components, automatic code splitting. Tradeoff: Steeper learning curve for App Router patterns, requires understanding of server vs client components.
- **CRA**: Simple setup, widely known. Tradeoff: No longer maintained, no SSR, manual routing setup, slower build times.
- **Vite + React Router**: Fast dev server, flexible. Tradeoff: More manual configuration, no SSR out of box, requires additional setup for production optimization.
- **Remix**: Full-stack framework, excellent data loading. Tradeoff: Opinionated, requires backend integration, overkill for frontend-only scope.

**Chosen Approach**: Next.js 14+ with App Router

**Rationale**:
- App Router provides modern React patterns (Server Components, Suspense boundaries)
- Built-in routing with file-system conventions reduces boilerplate
- Excellent TypeScript support and developer experience
- Automatic code splitting and optimization for performance goals (<3s page load)
- Large ecosystem and community support
- Aligns with existing skills documentation (nextjs-app-architecture.md)
- Production-ready with minimal configuration

### Decision 2: Styling Approach - Tailwind CSS with shadcn/ui

**Options Considered**:
1. **Tailwind CSS + shadcn/ui** (Chosen)
2. CSS Modules
3. Styled Components
4. Material-UI (MUI)

**Tradeoffs**:
- **Tailwind CSS + shadcn/ui**: Utility-first CSS, highly customizable, copy-paste components, no runtime overhead. Tradeoff: Verbose class names, requires learning utility classes.
- **CSS Modules**: Scoped styles, familiar CSS syntax. Tradeoff: More files to manage, no design system out of box, manual responsive design.
- **Styled Components**: CSS-in-JS, dynamic styling. Tradeoff: Runtime overhead, larger bundle size, Flash of Unstyled Content (FOUC) risk.
- **Material-UI**: Complete component library, consistent design. Tradeoff: Opinionated design, larger bundle size, harder to customize, may not meet performance goals.

**Chosen Approach**: Tailwind CSS with shadcn/ui

**Rationale**:
- Tailwind CSS provides utility-first approach for rapid UI development
- shadcn/ui offers accessible, customizable components (copy-paste, not npm dependency)
- Zero runtime overhead meets performance constraints (<200ms UI response)
- Excellent responsive design support for mobile-first approach
- Strong TypeScript integration
- Aligns with ui-components-design-system.md skill
- Smaller bundle size compared to component libraries
- Easy to customize for brand consistency

### Decision 3: State Management Approach - React Query + React Context

**Options Considered**:
1. **TanStack React Query + React Context** (Chosen)
2. Redux Toolkit
3. Zustand
4. Jotai/Recoil

**Tradeoffs**:
- **React Query + Context**: Server state managed by React Query (caching, invalidation, optimistic updates), client state in Context. Tradeoff: Two state management approaches, requires understanding of server vs client state.
- **Redux Toolkit**: Centralized state, predictable updates, DevTools. Tradeoff: Boilerplate for simple operations, overkill for this scope, manual cache management.
- **Zustand**: Minimal boilerplate, simple API. Tradeoff: No built-in server state management, manual API integration, less opinionated.
- **Jotai/Recoil**: Atomic state management, fine-grained updates. Tradeoff: Learning curve, less mature ecosystem, manual server state handling.

**Chosen Approach**: TanStack React Query for server state + React Context for client state

**Rationale**:
- React Query excels at server state management (API data, caching, background refetching)
- Automatic cache invalidation and optimistic updates meet <2s task operation goal
- Built-in loading and error states simplify UI implementation
- React Context sufficient for simple client state (UI toggles, filters)
- Minimal boilerplate compared to Redux
- Aligns with client-api-auth-handling.md skill (useApiQuery, useApiMutation hooks)
- Reduces bundle size by avoiding heavy state management libraries
- Excellent TypeScript support

### Decision 4: Routing and Layout Strategy - App Router with Route Groups

**Options Considered**:
1. **Next.js App Router with Route Groups** (Chosen)
2. Next.js Pages Router
3. React Router v6

**Tradeoffs**:
- **App Router with Route Groups**: File-system routing, nested layouts, route groups for shared layouts, server/client component flexibility. Tradeoff: Newer API, requires understanding of App Router conventions.
- **Pages Router**: Stable, well-documented, simpler mental model. Tradeoff: Less flexible layouts, no Server Components, older patterns.
- **React Router v6**: Framework-agnostic, flexible. Tradeoff: Manual setup, no SSR, requires additional configuration for code splitting.

**Chosen Approach**: Next.js App Router with Route Groups

**Rationale**:
- Route groups `(auth)` and `(dashboard)` enable shared layouts without affecting URL structure
- Nested layouts reduce code duplication (dashboard layout with auth check)
- File-system routing provides clear structure and reduces boilerplate
- Server Components for static content (landing page) improve performance
- Client Components for interactive features (task list, forms)
- Aligns with Next.js 14+ best practices and nextjs-app-architecture.md skill
- Supports protected routes with layout-level authentication checks

### Decision 5: Authentication Integration - Better Auth with JWT

**Options Considered**:
1. **Better Auth with JWT tokens** (Chosen)
2. NextAuth.js
3. Clerk
4. Custom auth implementation

**Tradeoffs**:
- **Better Auth with JWT**: Flexible, works with any backend, JWT token management, session handling. Tradeoff: Manual JWT integration with FastAPI backend, requires custom token endpoint.
- **NextAuth.js**: Popular, many providers, built-in session management. Tradeoff: Opinionated, requires backend adapter, may not integrate cleanly with FastAPI JWT.
- **Clerk**: Managed auth service, excellent UX. Tradeoff: External dependency, cost, vendor lock-in, may not work with existing FastAPI backend.
- **Custom auth**: Full control. Tradeoff: Security risks, reinventing the wheel, more code to maintain.

**Chosen Approach**: Better Auth with JWT tokens

**Rationale**:
- Better Auth provides session management on frontend while allowing JWT tokens for backend API calls
- Flexible integration with FastAPI backend (custom JWT endpoint)
- Supports email/password authentication (FR-001, FR-004)
- Built-in session hooks (useSession, useAuth) simplify component logic
- Aligns with jwt-better-auth-integration.md and client-api-auth-handling.md skills
- Automatic token attachment to API requests via custom API client
- Handles token refresh and session expiration (edge case from spec)
- No vendor lock-in, works with existing backend architecture

## Testing & Validation Strategy

### Acceptance Checks Aligned with Success Criteria

**From Spec Success Criteria (SC-001 to SC-010)**:

1. **SC-001: Registration completion < 1 minute**
   - E2E test: Measure time from landing page → signup form → dashboard
   - Acceptance: Average completion time < 60 seconds

2. **SC-002: Task creation < 10 seconds**
   - E2E test: Measure time from dashboard → add task → task appears in list
   - Acceptance: Average completion time < 10 seconds

3. **SC-003: Task list updates within 2 seconds**
   - Integration test: Mock API response, measure React Query cache update time
   - Acceptance: UI reflects changes within 2 seconds of user action

4. **SC-004: Application load < 3 seconds**
   - Performance test: Lighthouse CI, measure First Contentful Paint (FCP) and Time to Interactive (TTI)
   - Acceptance: FCP < 1.5s, TTI < 3s on standard broadband

5. **SC-005: 95% first-attempt success rate**
   - User testing: Track form submission success rates
   - Acceptance: 95% of users successfully create first task without errors

6. **SC-006: Performance with 100 tasks**
   - Load test: Render task list with 100 items, measure render time and scroll performance
   - Acceptance: Smooth 60fps scrolling, <500ms initial render

7. **SC-007: Cross-browser and mobile compatibility**
   - Browser testing: Playwright tests on Chrome, Firefox, Safari, Edge
   - Mobile testing: Responsive design tests on iOS Safari, Android Chrome
   - Acceptance: All functional requirements work on all target browsers

8. **SC-008: Zero token exposure**
   - Security audit: Check browser console, localStorage, sessionStorage, network tab
   - Acceptance: No JWT tokens or sensitive data visible in browser tools

9. **SC-009: Keyboard accessibility**
   - Accessibility test: Navigate entire app using only keyboard (Tab, Enter, Escape)
   - Acceptance: All interactive elements reachable and operable via keyboard

10. **SC-010: 100% error message coverage**
    - Error handling test: Trigger all error scenarios (network failure, validation errors, API errors)
    - Acceptance: User-friendly error message displayed for every failure case

### Visual Validation

**Layout and Responsiveness**:
- Visual regression testing using Playwright screenshots
- Test breakpoints: Mobile (375px), Tablet (768px), Desktop (1024px, 1440px)
- Verify layouts match design specifications at each breakpoint
- Check for text overflow, image scaling, button sizing
- Validate touch targets (minimum 44x44px on mobile)

**Component Consistency**:
- Storybook for component documentation and visual testing
- Verify consistent spacing, colors, typography across components
- Check hover states, focus states, active states
- Validate loading states (spinners, skeletons) and error states

### Component-Level Validation

**Reusability Checks**:
- Unit tests for all reusable components (Button, Input, Card, Modal)
- Verify components accept props correctly and render expected output
- Test component composition (nested components)
- Validate TypeScript prop types and default values

**Consistency Checks**:
- Verify all components use Tailwind CSS utility classes consistently
- Check that shadcn/ui components are customized consistently
- Validate consistent error handling patterns across forms
- Ensure consistent loading state patterns across async operations

### User Flow Validation

**Authentication-Protected Routes**:
- E2E test: Attempt to access dashboard without authentication → redirected to login
- E2E test: Login → redirected to dashboard → logout → redirected to login
- E2E test: Session expiration → redirected to login with message
- Integration test: Verify ProtectedRoute component redirects unauthenticated users

**Task Management Flows**:
- E2E test: Create task → verify appears in list → mark complete → verify visual change
- E2E test: Edit task → verify updated title → delete task → verify removed from list
- E2E test: Filter tasks (active/completed) → verify correct tasks shown
- E2E test: Search tasks → verify matching tasks displayed

**Error Recovery Flows**:
- E2E test: Network failure during task creation → error message → retry → success
- E2E test: Invalid form input → validation error → correct input → success
- E2E test: API error (500) → user-friendly error message displayed

### Accessibility Checks

**WCAG 2.1 Level AA Compliance**:
- Automated testing: axe-core integration in Jest and Playwright
- Color contrast: Verify all text meets 4.5:1 contrast ratio
- Focus indicators: Verify visible focus outlines on all interactive elements
- ARIA labels: Verify screen reader compatibility for all components
- Semantic HTML: Verify proper heading hierarchy, landmark regions

**Keyboard Navigation**:
- Tab order: Verify logical tab order through all interactive elements
- Keyboard shortcuts: Verify Enter submits forms, Escape closes modals
- Focus management: Verify focus moves to appropriate element after actions (e.g., modal close returns focus)

### Performance Checks

**Bundle Size**:
- Webpack Bundle Analyzer: Verify total bundle size < 500KB (gzipped)
- Code splitting: Verify route-based code splitting working correctly
- Tree shaking: Verify unused code removed from production bundle

**Runtime Performance**:
- React DevTools Profiler: Identify unnecessary re-renders
- Chrome DevTools Performance: Verify 60fps during animations and scrolling
- Lighthouse CI: Verify performance score > 90

**Network Performance**:
- Verify API requests use proper caching headers
- Verify React Query cache reduces redundant API calls
- Verify optimistic updates provide instant feedback

## Technical Details

### Research-Concurrent Approach

This plan follows a research-concurrent approach where design and validation happen alongside implementation planning:

- **Phase 0 (Research)**: Validate technology choices, prototype authentication flow, test API integration patterns
- **Phase 1 (Design & Contracts)**: Define data models, API contracts, component architecture
- **Phase 2-5 (Implementation)**: Build features incrementally with continuous validation

### Implementation Phases

#### Phase 0: Foundation (Project Setup, Layout, Routing)

**Objectives**:
- Initialize Next.js 14+ project with TypeScript and Tailwind CSS
- Set up project structure and configuration files
- Implement root layout and basic routing
- Configure development environment

**Deliverables**:
- Next.js project initialized with App Router
- Tailwind CSS and shadcn/ui configured
- TypeScript configuration with strict mode
- ESLint and Prettier configured
- Root layout with basic navigation
- Landing page (public route)
- Route groups for auth and dashboard

**Validation**:
- Project builds without errors
- Development server runs successfully
- Tailwind CSS utilities work correctly
- TypeScript type checking passes

#### Phase 1: Core UI (Components, Pages, Styling)

**Objectives**:
- Build reusable UI components using shadcn/ui
- Implement authentication pages (login, signup)
- Implement dashboard layout and task list page
- Apply responsive design for mobile, tablet, desktop

**Deliverables**:
- UI components: Button, Input, Card, Modal, Checkbox, Form
- Auth pages: Login page, Signup page with forms and validation
- Dashboard layout: Header, navigation, protected route wrapper
- Task list page: Empty state, task items, loading states
- Responsive design: Mobile-first approach with breakpoints

**Validation**:
- Components render correctly in Storybook
- Forms validate input correctly (client-side)
- Responsive design works on all breakpoints
- Visual regression tests pass

#### Phase 2: Integration (Auth Flow, API Consumption)

**Objectives**:
- Integrate Better Auth for authentication
- Implement API client with JWT token handling
- Connect authentication pages to backend API
- Implement task CRUD operations with API integration
- Set up React Query for server state management

**Deliverables**:
- Better Auth client configured with JWT endpoint
- API client with automatic token attachment
- useAuth hook for session management
- useApiQuery and useApiMutation hooks
- Authentication flows: signup, login, logout
- Task operations: create, read, update, delete
- Error handling and loading states

**Validation**:
- Authentication flow works end-to-end
- JWT tokens attached to API requests correctly
- Task operations persist to backend
- Error messages display for failed operations
- Loading states display during async operations

#### Phase 3: Advanced Features (Task Completion, Edit/Delete, Filtering)

**Objectives**:
- Implement task completion toggle
- Implement task edit and delete functionality
- Implement task filtering (active, completed, all)
- Implement task search functionality
- Add confirmation dialogs for destructive actions

**Deliverables**:
- Task completion checkbox with optimistic updates
- Task edit modal with form validation
- Task delete with confirmation dialog
- Filter buttons: All, Active, Completed
- Search input with debounced filtering
- Optimistic UI updates for better UX

**Validation**:
- Task completion updates immediately (optimistic)
- Edit and delete operations work correctly
- Filters show correct subset of tasks
- Search filters tasks by title
- Confirmation dialogs prevent accidental deletions

#### Phase 4: Polish & Validation (Responsiveness, UX Improvements)

**Objectives**:
- Refine responsive design and mobile UX
- Improve loading states and error messages
- Add animations and transitions
- Implement accessibility improvements
- Optimize performance (bundle size, render performance)
- Conduct comprehensive testing

**Deliverables**:
- Smooth animations for task operations (add, complete, delete)
- Improved loading states (skeleton screens)
- Better error messages with recovery actions
- Keyboard navigation support
- Focus management for modals and forms
- Performance optimizations (code splitting, lazy loading)
- Comprehensive test suite (unit, integration, E2E)

**Validation**:
- All success criteria (SC-001 to SC-010) met
- Accessibility audit passes (WCAG 2.1 AA)
- Performance audit passes (Lighthouse score > 90)
- Cross-browser testing passes
- E2E test suite passes on all target browsers
- Visual regression tests pass

## Deliverable

This structured frontend implementation plan provides:

1. **Clear Architecture**: Next.js App Router with route groups, component-based structure, separation of concerns
2. **Technology Decisions**: Justified choices for framework, styling, state management, routing, and authentication
3. **Implementation Roadmap**: Four phases from foundation to polish with clear objectives and deliverables
4. **Validation Strategy**: Comprehensive testing approach aligned with spec success criteria
5. **Agent Integration**: Defined workflow for frontend sub-agent with reusable skills

**Next Steps**:
- Run `/sp.tasks` to convert this plan into actionable, dependency-ordered tasks
- Generate `research.md` for Phase 0 technology validation
- Generate `data-model.md` for frontend data structures
- Generate `contracts/` for API contract definitions
- Generate `quickstart.md` for development setup guide

**Ready for**: Task generation and implementation by `nextjs-frontend-implementer` agent
