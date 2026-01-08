# Quickstart Guide: Todo Web Application Frontend

**Feature**: 001-todo-frontend | **Date**: 2026-01-07 | **Version**: 1.0

## Purpose

Get the Todo Web Application frontend up and running quickly for development. This guide covers initial setup, configuration, and common development tasks.

## Prerequisites

### Required Software

- **Node.js**: v18.17.0 or higher (LTS recommended)
- **npm**: v9.0.0 or higher (comes with Node.js)
- **Git**: Latest version
- **Code Editor**: VS Code recommended (with extensions below)

### Recommended VS Code Extensions

- ESLint (`dbaeumer.vscode-eslint`)
- Prettier (`esbenp.prettier-vscode`)
- Tailwind CSS IntelliSense (`bradlc.vscode-tailwindcss`)
- TypeScript Vue Plugin (Volar) (`Vue.volar`)

### Backend Requirements

The frontend requires a running FastAPI backend with the following endpoints:
- Authentication: `/api/auth/signup`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/get-jwt`
- Tasks: `/api/v1/tasks` (GET, POST, PUT, PATCH, DELETE)

See `contracts/auth-api.md` and `contracts/tasks-api.md` for full API specifications.

## Initial Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackhton-II
git checkout 001-todo-frontend
```

### 2. Navigate to Frontend Directory

```bash
cd frontend
```

### 3. Install Dependencies

```bash
npm install
```

This will install:
- Next.js 14+
- React 18+
- TypeScript
- Tailwind CSS
- Better Auth
- TanStack React Query
- shadcn/ui components
- Development tools (ESLint, Prettier)

### 4. Configure Environment Variables

Create `.env.local` file in the `frontend` directory:

```bash
cp .env.example .env.local
```

Edit `.env.local` with your configuration:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production
BETTER_AUTH_URL=http://localhost:3000

# Environment
NODE_ENV=development
```

**Important**: Never commit `.env.local` to version control. It's already in `.gitignore`.

### 5. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Project Structure

```
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
│   │   └── layout/           # Layout components
│   ├── lib/                  # Utilities and configurations
│   │   ├── auth/             # Better Auth client setup
│   │   ├── api/              # API client with JWT handling
│   │   └── utils/            # Helper functions
│   ├── hooks/                # Custom React hooks
│   ├── types/                # TypeScript type definitions
│   └── styles/               # Global styles
├── public/                   # Static assets
├── tests/                    # Test files
├── .env.local               # Environment variables (gitignored)
├── .env.example             # Environment variables template
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies
```

## Common Development Tasks

### Running the Development Server

```bash
npm run dev
```

- Hot reload enabled
- TypeScript type checking in watch mode
- Tailwind CSS compilation

### Building for Production

```bash
npm run build
```

This creates an optimized production build in `.next/` directory.

### Starting Production Server

```bash
npm run start
```

Serves the production build. Run `npm run build` first.

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

### Linting and Formatting

```bash
# Run ESLint
npm run lint

# Fix ESLint errors
npm run lint:fix

# Format code with Prettier
npm run format

# Check formatting
npm run format:check
```

### Type Checking

```bash
# Run TypeScript type checker
npm run type-check
```

### Adding shadcn/ui Components

```bash
# Add a new component (e.g., button)
npx shadcn-ui@latest add button

# Add multiple components
npx shadcn-ui@latest add button input card
```

Components are copied to `src/components/ui/` and can be customized.

## Development Workflow

### 1. Create a New Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit files in `src/` directory. The dev server will hot reload automatically.

### 3. Test Your Changes

```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e

# Check types
npm run type-check

# Lint code
npm run lint
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: your feature description"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## API Integration

### Using the API Client

```typescript
// Import API client
import { api } from "@/lib/api/client"

// Make GET request
const tasks = await api.get<Task[]>("/api/v1/tasks")

// Make POST request
const newTask = await api.post<Task>("/api/v1/tasks", { title: "New task" })

// Make PATCH request
const updatedTask = await api.patch<Task>(`/api/v1/tasks/${id}`, { completed: true })

// Make DELETE request
await api.delete(`/api/v1/tasks/${id}`)
```

### Using React Query Hooks

```typescript
// Import hooks
import { useTasks, useCreateTask, useToggleTaskComplete } from "@/hooks/useTasks"

// In component
function TaskList() {
  const { data: tasks, isLoading, error } = useTasks()
  const createTask = useCreateTask()
  const toggleComplete = useToggleTaskComplete()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      {tasks.map(task => (
        <div key={task.id}>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => toggleComplete.mutate({ id: task.id, completed: !task.completed })}
          />
          <span>{task.title}</span>
        </div>
      ))}
    </div>
  )
}
```

### Using Authentication

```typescript
// Import auth hooks
import { useAuth } from "@/lib/auth/client"

// In component
function Dashboard() {
  const { user, isAuthenticated, isLoading } = useAuth()

  if (isLoading) return <div>Loading...</div>
  if (!isAuthenticated) return <div>Please log in</div>

  return <div>Welcome, {user.name}!</div>
}
```

## Troubleshooting

### Port Already in Use

If port 3000 is already in use:

```bash
# Kill process on port 3000 (Linux/Mac)
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 npm run dev
```

### Module Not Found Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors

```bash
# Restart TypeScript server in VS Code
# Command Palette (Ctrl+Shift+P) → "TypeScript: Restart TS Server"

# Or rebuild
npm run build
```

### Tailwind CSS Not Working

```bash
# Ensure Tailwind is properly configured
# Check tailwind.config.js content paths
# Restart dev server
npm run dev
```

### API Connection Issues

1. Verify backend is running at `http://localhost:8000`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Check browser console for CORS errors
4. Verify JWT token is being attached to requests (Network tab)

### Better Auth Session Issues

1. Clear browser cookies and localStorage
2. Verify `BETTER_AUTH_SECRET` is set in `.env.local`
3. Check backend `/api/auth/get-jwt` endpoint is working
4. Verify session cookie is being set (Application tab → Cookies)

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_APP_URL` | Frontend app URL | `http://localhost:3000` |
| `BETTER_AUTH_SECRET` | Secret key for Better Auth | `your-secret-key-here` |
| `BETTER_AUTH_URL` | Better Auth callback URL | `http://localhost:3000` |
| `NODE_ENV` | Environment mode | `development` or `production` |

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Never put secrets in these variables.

## Useful Commands Reference

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm test` | Run tests |
| `npm run lint` | Run ESLint |
| `npm run type-check` | Run TypeScript type checker |
| `npm run format` | Format code with Prettier |
| `npx shadcn-ui@latest add <component>` | Add shadcn/ui component |

## Next Steps

1. **Read the Specification**: Review `specs/001-todo-frontend/spec.md` for requirements
2. **Review the Plan**: Check `specs/001-todo-frontend/plan.md` for architecture decisions
3. **Understand Data Model**: Read `specs/001-todo-frontend/data-model.md` for types and state management
4. **Review API Contracts**: Check `specs/001-todo-frontend/contracts/` for API specifications
5. **Start Implementation**: Begin with Phase 0 (Foundation) from the plan

## Getting Help

- **Documentation**: Check `specs/001-todo-frontend/` directory
- **Skills Reference**: Review `.claude/skills/` for implementation patterns
- **API Contracts**: See `specs/001-todo-frontend/contracts/` for backend integration
- **Issues**: Create GitHub issue for bugs or questions

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [Better Auth Documentation](https://better-auth.com)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-07 | Initial quickstart guide |
