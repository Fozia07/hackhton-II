# Todo Web Application Frontend

A responsive, authenticated web frontend for a multi-user Todo application built with Next.js 14+, React, TypeScript, and Tailwind CSS.

## Features

- User authentication (sign up, sign in, sign out)
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Filter tasks (all, active, completed)
- Search tasks by title
- Responsive design for mobile, tablet, and desktop

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui-inspired components
- **State Management**: TanStack React Query for server state, React Context for client state
- **Authentication**: Custom JWT-based authentication with backend integration
- **Forms**: Custom form components with validation

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory: `cd phaseII/frontend`
3. Install dependencies:

```bash
npm install
```

4. Create a `.env.local` file based on `.env.example`:

```bash
cp .env.example .env.local
```

5. Update the environment variables in `.env.local`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_URL=http://localhost:3001

# Environment
NODE_ENV=development
```

**Important**: Ensure `NEXT_PUBLIC_API_URL` points to your local backend (http://localhost:8001) for development.

### Running the Development Server

```bash
npm run dev
```

The application will be available at [http://localhost:3001](http://localhost:3001).

### Building for Production

```bash
npm run build
```

### Running the Production Server

```bash
npm start
```

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL | http://localhost:8001 (dev) or https://your-backend.railway.app (prod) |
| `NEXT_PUBLIC_APP_URL` | Yes | Frontend URL | http://localhost:3001 (dev) or https://your-app.vercel.app (prod) |
| `NODE_ENV` | No | Environment | development or production |

**Note**: All environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

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
│   │   ├── ui/               # Base UI components
│   │   ├── auth/             # Auth-related components
│   │   ├── tasks/            # Task-related components
│   │   └── layout/           # Layout components
│   ├── contexts/              # React Context providers
│   ├── hooks/                 # Custom React hooks
│   ├── lib/                  # Utilities and configurations
│   ├── types/                # TypeScript type definitions
│   └── styles/               # Global styles
├── public/                   # Static assets
├── .env.example             # Environment variables template
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies
```

## API Integration

The frontend communicates with a JWT-secured FastAPI backend via REST API. Update the `NEXT_PUBLIC_API_URL` in your environment variables to point to your backend API.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.