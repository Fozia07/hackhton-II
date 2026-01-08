# Next.js App Architecture & Routing

## Expertise
Expert skill for implementing Next.js App Router architecture and file-based routing. Specializes in Server Components, Client Components, layouts, loading states, error boundaries, and predictable folder organization following Next.js 16+ conventions.

## Purpose
This skill handles Next.js application structure and routing, enabling you to:
- Implement App Router file-based routing
- Use Server Components by default
- Use Client Components only when necessary
- Create layouts and nested layouts
- Implement loading and error states
- Organize routes with route groups
- Follow Next.js conventions and best practices
- Structure folders predictably

## When to Use
Use this skill when you need to:
- Set up Next.js App Router structure
- Create new pages and routes
- Implement layouts and nested layouts
- Add loading and error boundaries
- Organize routes with route groups
- Implement parallel routes or intercepting routes
- Structure the app directory
- Follow Next.js file conventions

## Core Concepts

### App Router File Structure

```
app/
├── layout.tsx              # Root layout (required)
├── page.tsx                # Home page (/)
├── loading.tsx             # Loading UI for home
├── error.tsx               # Error boundary for home
├── not-found.tsx           # 404 page
├── global-error.tsx        # Global error boundary
│
├── (auth)/                 # Route group (doesn't affect URL)
│   ├── layout.tsx          # Auth layout
│   ├── login/
│   │   └── page.tsx        # /login
│   └── signup/
│       └── page.tsx        # /signup
│
├── dashboard/
│   ├── layout.tsx          # Dashboard layout
│   ├── page.tsx            # /dashboard
│   ├── loading.tsx         # Loading for dashboard
│   ├── error.tsx           # Error boundary for dashboard
│   │
│   ├── settings/
│   │   └── page.tsx        # /dashboard/settings
│   │
│   └── [userId]/           # Dynamic route
│       ├── page.tsx        # /dashboard/[userId]
│       └── posts/
│           └── page.tsx    # /dashboard/[userId]/posts
│
└── api/                    # API routes
    └── auth/
        └── [...all]/
            └── route.ts    # /api/auth/*
```

### Server vs Client Components

**Server Components (Default)**:
```tsx
// app/page.tsx
// Server Component by default - NO "use client" directive

import { db } from "@/lib/db";

export default async function HomePage() {
  // Can directly access database
  const posts = await db.post.findMany();

  return (
    <div>
      <h1>Posts</h1>
      {posts.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  );
}
```

**Client Components (When Needed)**:
```tsx
// app/components/counter.tsx
"use client"; // Required for interactivity

import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

**When to Use Client Components**:
- Event handlers (onClick, onChange, etc.)
- State (useState, useReducer)
- Effects (useEffect)
- Browser APIs (localStorage, window, etc.)
- Custom hooks that use the above

**When to Use Server Components**:
- Fetching data
- Accessing backend resources directly
- Keeping sensitive information on server
- Reducing client-side JavaScript
- Everything else (default)

## File Conventions

### 1. Root Layout (Required)

**app/layout.tsx**:
```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "My App",
  description: "My application description",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
```

### 2. Pages

**app/page.tsx** (Home page):
```tsx
export default function HomePage() {
  return (
    <div>
      <h1>Welcome</h1>
      <p>This is the home page</p>
    </div>
  );
}
```

**app/about/page.tsx** (/about):
```tsx
export default function AboutPage() {
  return (
    <div>
      <h1>About</h1>
      <p>About our company</p>
    </div>
  );
}
```

### 3. Nested Layouts

**app/dashboard/layout.tsx**:
```tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <nav>
        <a href="/dashboard">Dashboard</a>
        <a href="/dashboard/settings">Settings</a>
      </nav>
      <main>{children}</main>
    </div>
  );
}
```

**app/dashboard/page.tsx**:
```tsx
export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome to your dashboard</p>
    </div>
  );
}
```

### 4. Loading States

**app/dashboard/loading.tsx**:
```tsx
export default function DashboardLoading() {
  return (
    <div>
      <p>Loading dashboard...</p>
    </div>
  );
}
```

**With Suspense Boundaries**:
```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";
import { PostList } from "./post-list";
import { UserStats } from "./user-stats";

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Independent loading states */}
      <Suspense fallback={<div>Loading posts...</div>}>
        <PostList />
      </Suspense>

      <Suspense fallback={<div>Loading stats...</div>}>
        <UserStats />
      </Suspense>
    </div>
  );
}
```

### 5. Error Boundaries

**app/dashboard/error.tsx**:
```tsx
"use client"; // Error boundaries must be Client Components

import { useEffect } from "react";

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to error reporting service
    console.error(error);
  }, [error]);

  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>
        Try again
      </button>
    </div>
  );
}
```

**Global Error Boundary** (app/global-error.tsx):
```tsx
"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  );
}
```

### 6. Not Found Pages

**app/not-found.tsx**:
```tsx
export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
    </div>
  );
}
```

**Programmatic Not Found**:
```tsx
// app/posts/[id]/page.tsx
import { notFound } from "next/navigation";

export default async function PostPage({
  params,
}: {
  params: { id: string };
}) {
  const post = await getPost(params.id);

  if (!post) {
    notFound(); // Triggers not-found.tsx
  }

  return <div>{post.title}</div>;
}
```

## Dynamic Routes

### 1. Single Dynamic Segment

**app/posts/[id]/page.tsx** (/posts/123):
```tsx
export default function PostPage({
  params,
}: {
  params: { id: string };
}) {
  return (
    <div>
      <h1>Post {params.id}</h1>
    </div>
  );
}
```

### 2. Multiple Dynamic Segments

**app/blog/[category]/[slug]/page.tsx** (/blog/tech/nextjs-guide):
```tsx
export default function BlogPostPage({
  params,
}: {
  params: { category: string; slug: string };
}) {
  return (
    <div>
      <h1>Category: {params.category}</h1>
      <h2>Slug: {params.slug}</h2>
    </div>
  );
}
```

### 3. Catch-All Segments

**app/docs/[...slug]/page.tsx** (/docs/a/b/c):
```tsx
export default function DocsPage({
  params,
}: {
  params: { slug: string[] };
}) {
  return (
    <div>
      <h1>Docs</h1>
      <p>Path: {params.slug.join("/")}</p>
    </div>
  );
}
```

### 4. Optional Catch-All Segments

**app/shop/[[...slug]]/page.tsx** (/shop or /shop/a/b):
```tsx
export default function ShopPage({
  params,
}: {
  params: { slug?: string[] };
}) {
  return (
    <div>
      <h1>Shop</h1>
      {params.slug ? (
        <p>Path: {params.slug.join("/")}</p>
      ) : (
        <p>All products</p>
      )}
    </div>
  );
}
```

## Route Groups

**Purpose**: Organize routes without affecting URL structure

### Basic Route Group

```
app/
├── (marketing)/
│   ├── layout.tsx          # Marketing layout
│   ├── page.tsx            # / (home)
│   ├── about/
│   │   └── page.tsx        # /about
│   └── contact/
│       └── page.tsx        # /contact
│
└── (shop)/
    ├── layout.tsx          # Shop layout
    ├── products/
    │   └── page.tsx        # /products
    └── cart/
        └── page.tsx        # /cart
```

**app/(marketing)/layout.tsx**:
```tsx
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <header>Marketing Header</header>
      {children}
      <footer>Marketing Footer</footer>
    </div>
  );
}
```

**app/(shop)/layout.tsx**:
```tsx
export default function ShopLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <header>Shop Header</header>
      {children}
      <footer>Shop Footer</footer>
    </div>
  );
}
```

### Multiple Root Layouts

```
app/
├── (main)/
│   ├── layout.tsx          # Main layout
│   └── page.tsx            # /
│
└── (admin)/
    ├── layout.tsx          # Admin layout (different root)
    └── page.tsx            # /admin
```

## Parallel Routes

**Purpose**: Render multiple pages in the same layout simultaneously

```
app/
├── layout.tsx
├── page.tsx
├── @team/
│   └── page.tsx
└── @analytics/
    └── page.tsx
```

**app/layout.tsx**:
```tsx
export default function Layout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode;
  team: React.ReactNode;
  analytics: React.ReactNode;
}) {
  return (
    <div>
      <div>{children}</div>
      <div>{team}</div>
      <div>{analytics}</div>
    </div>
  );
}
```

## Intercepting Routes

**Purpose**: Intercept a route and show it in a modal while keeping URL

```
app/
├── feed/
│   └── page.tsx            # /feed
├── photo/
│   └── [id]/
│       └── page.tsx        # /photo/123
└── @modal/
    └── (.)photo/
        └── [id]/
            └── page.tsx    # Intercepts /photo/123 in modal
```

## Metadata and SEO

### Static Metadata

**app/page.tsx**:
```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Home",
  description: "Welcome to our site",
};

export default function HomePage() {
  return <div>Home</div>;
}
```

### Dynamic Metadata

**app/posts/[id]/page.tsx**:
```tsx
import type { Metadata } from "next";

export async function generateMetadata({
  params,
}: {
  params: { id: string };
}): Promise<Metadata> {
  const post = await getPost(params.id);

  return {
    title: post.title,
    description: post.excerpt,
  };
}

export default function PostPage({
  params,
}: {
  params: { id: string };
}) {
  return <div>Post {params.id}</div>;
}
```

### OpenGraph and Twitter Cards

```tsx
export const metadata: Metadata = {
  title: "My Post",
  description: "Post description",
  openGraph: {
    title: "My Post",
    description: "Post description",
    images: ["/og-image.jpg"],
  },
  twitter: {
    card: "summary_large_image",
    title: "My Post",
    description: "Post description",
    images: ["/twitter-image.jpg"],
  },
};
```

## Navigation

### Link Component

```tsx
import Link from "next/link";

export function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/posts/123">Post 123</Link>
    </nav>
  );
}
```

### Programmatic Navigation

```tsx
"use client";

import { useRouter } from "next/navigation";

export function NavigateButton() {
  const router = useRouter();

  return (
    <button onClick={() => router.push("/dashboard")}>
      Go to Dashboard
    </button>
  );
}
```

### usePathname and useSearchParams

```tsx
"use client";

import { usePathname, useSearchParams } from "next/navigation";

export function CurrentRoute() {
  const pathname = usePathname(); // /dashboard/settings
  const searchParams = useSearchParams(); // ?tab=profile

  return (
    <div>
      <p>Current path: {pathname}</p>
      <p>Tab: {searchParams.get("tab")}</p>
    </div>
  );
}
```

## Component Organization

### Recommended Structure

```
app/
├── (routes)/               # Route groups for pages
│   ├── (auth)/
│   ├── (dashboard)/
│   └── (marketing)/
│
├── components/             # Shared components
│   ├── ui/                 # UI components
│   ├── forms/              # Form components
│   └── layouts/            # Layout components
│
└── lib/                    # Utilities (not components)
```

### Co-located Components

```
app/
└── dashboard/
    ├── page.tsx            # Dashboard page
    ├── layout.tsx          # Dashboard layout
    ├── loading.tsx         # Loading state
    ├── error.tsx           # Error boundary
    │
    ├── components/         # Dashboard-specific components
    │   ├── stats-card.tsx
    │   └── activity-feed.tsx
    │
    └── settings/
        └── page.tsx        # Settings page
```

## Best Practices

### 1. Server Components by Default
```tsx
// ✅ Good - Server Component (default)
export default async function PostsPage() {
  const posts = await getPosts();
  return <PostList posts={posts} />;
}

// ❌ Bad - Unnecessary Client Component
"use client";
export default function PostsPage() {
  // No interactivity needed
  return <div>Posts</div>;
}
```

### 2. Composition Pattern

```tsx
// ✅ Good - Server Component with Client Component children
// app/page.tsx (Server Component)
import { ClientCounter } from "./client-counter";

export default async function HomePage() {
  const data = await getData();

  return (
    <div>
      <h1>Server Data: {data}</h1>
      <ClientCounter /> {/* Client Component */}
    </div>
  );
}

// app/client-counter.tsx (Client Component)
"use client";
import { useState } from "react";

export function ClientCounter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### 3. Loading States

```tsx
// ✅ Good - Granular loading with Suspense
import { Suspense } from "react";

export default function Page() {
  return (
    <div>
      <Suspense fallback={<div>Loading posts...</div>}>
        <Posts />
      </Suspense>

      <Suspense fallback={<div>Loading comments...</div>}>
        <Comments />
      </Suspense>
    </div>
  );
}

// ❌ Bad - Single loading state for everything
export default function Page() {
  return (
    <div>
      <Posts />
      <Comments />
    </div>
  );
}
// Uses loading.tsx which blocks entire page
```

### 4. Error Boundaries

```tsx
// ✅ Good - Specific error boundaries
app/
├── dashboard/
│   ├── error.tsx           # Catches dashboard errors
│   └── settings/
│       └── error.tsx       # Catches settings errors

// ❌ Bad - Only root error boundary
app/
└── error.tsx               # Catches all errors (too broad)
```

### 5. Route Organization

```tsx
// ✅ Good - Organized with route groups
app/
├── (auth)/
│   ├── login/
│   └── signup/
├── (dashboard)/
│   ├── overview/
│   └── settings/
└── (marketing)/
    ├── about/
    └── contact/

// ❌ Bad - Flat structure
app/
├── login/
├── signup/
├── overview/
├── settings/
├── about/
└── contact/
```

### 6. Metadata

```tsx
// ✅ Good - Dynamic metadata
export async function generateMetadata({ params }) {
  const post = await getPost(params.id);
  return {
    title: post.title,
    description: post.excerpt,
  };
}

// ❌ Bad - Static metadata for dynamic content
export const metadata = {
  title: "Post",
  description: "A post",
};
```

## Common Patterns

### 1. Protected Routes

```tsx
// app/dashboard/layout.tsx
import { redirect } from "next/navigation";
import { getSession } from "@/lib/auth";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getSession();

  if (!session) {
    redirect("/login");
  }

  return <div>{children}</div>;
}
```

### 2. Conditional Layouts

```tsx
// app/layout.tsx
import { getSession } from "@/lib/auth";
import { AuthenticatedNav } from "./authenticated-nav";
import { PublicNav } from "./public-nav";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getSession();

  return (
    <html>
      <body>
        {session ? <AuthenticatedNav /> : <PublicNav />}
        {children}
      </body>
    </html>
  );
}
```

### 3. Breadcrumbs

```tsx
// app/dashboard/[userId]/posts/[postId]/page.tsx
export default function PostPage({
  params,
}: {
  params: { userId: string; postId: string };
}) {
  return (
    <div>
      <nav>
        <a href="/dashboard">Dashboard</a> /
        <a href={`/dashboard/${params.userId}`}>User {params.userId}</a> /
        <a href={`/dashboard/${params.userId}/posts`}>Posts</a> /
        <span>Post {params.postId}</span>
      </nav>
    </div>
  );
}
```

## TypeScript Types

### Page Props

```tsx
type PageProps = {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
};

export default function Page({ params, searchParams }: PageProps) {
  return <div>Page {params.id}</div>;
}
```

### Layout Props

```tsx
type LayoutProps = {
  children: React.ReactNode;
  params: { id: string };
};

export default function Layout({ children, params }: LayoutProps) {
  return <div>{children}</div>;
}
```

### Error Props

```tsx
type ErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function Error({ error, reset }: ErrorProps) {
  return <div>Error: {error.message}</div>;
}
```

## Summary

This skill provides comprehensive guidance for Next.js App Router architecture and routing:

**Core Concepts:**
- Server Components by default
- Client Components only when needed
- File-based routing conventions
- Layouts and nested layouts
- Loading and error states

**Advanced Features:**
- Route groups for organization
- Parallel routes for simultaneous rendering
- Intercepting routes for modals
- Dynamic routes and catch-all segments
- Metadata and SEO optimization

**Best Practices:**
- Composition pattern for Server/Client Components
- Granular loading states with Suspense
- Specific error boundaries
- Organized route structure
- Dynamic metadata for SEO

Use this skill to build well-structured Next.js applications with proper routing, layouts, and component organization following Next.js 16+ conventions and best practices.
