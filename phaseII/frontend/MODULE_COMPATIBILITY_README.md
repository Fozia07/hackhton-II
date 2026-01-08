# Next.js 16.1.1 with Turbopack - Module Compatibility Guide

This document explains the module system configuration that resolves the CommonJS (CJS) and ECMAScript Module (ESM) compatibility issues.

## Configuration Overview

### Package.json
- `"type": "module"` - Enables ES module support throughout the project
- All dependencies are properly configured for ES module consumption

### Next.js Configuration (next.config.mjs)
- Uses ES module syntax with proper imports
- Configured for Turbopack with `turbopack: {}`
- Uses `serverExternalPackages: []` instead of deprecated experimental options

### TypeScript Configuration (tsconfig.json)
- `"module": "esnext"` - Specifies ES module syntax
- `"moduleResolution": "bundler"` - Uses modern module resolution
- `"verbatimModuleSyntax": true` - Ensures strict module compatibility

### PostCSS Configuration (postcss.config.js)
- Uses ES module export syntax (`export default`)
- Uses `@tailwindcss/postcss` plugin for Tailwind CSS v4 compatibility

### Tailwind CSS Configuration (tailwind.config.js)
- Uses ES module export syntax (`export default`)

## File Structure Conventions

```
src/
├── app/                 # Next.js App Router pages
│   ├── globals.css      # Global styles
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Home page
├── components/          # Reusable UI components
├── lib/                 # Utility functions
├── hooks/               # Custom React hooks
├── contexts/            # React context providers
├── types/               # TypeScript type definitions
└── styles/             # Shared styles
```

## Module Import/Export Patterns

### ES Module Imports (Recommended)
```ts
// Named exports
import { ComponentName } from '@/components/ComponentName'

// Default exports
import Component from '@/components/Component'

// Type imports
import type { SomeType } from '@/types/SomeType'
```

### ES Module Exports (Recommended)
```ts
// Named exports
export const ComponentName = () => { ... }

// Default exports
const Component = () => { ... }
export default Component

// Type exports
export type SomeType = { ... }
```

## Common Issues and Solutions

### Issue: "Specified module format (CommonJs) is not matching the module format of the source code (EcmaScript Modules)"
**Solution:** Ensure `package.json` has `"type": "module"` and all config files use ES module syntax (`import`/`export` instead of `require`/`module.exports`)

### Issue: PostCSS/Tailwind CSS plugin errors
**Solution:** Install `@tailwindcss/postcss` and update `postcss.config.js` to use the correct plugin name

### Issue: Webpack configuration conflicts with Turbopack
**Solution:** Simplify next.config.mjs for Turbopack usage, avoid webpack-specific configurations when possible

## Development Commands

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

Environment variables are loaded from `.env.local` and prefixed with `NEXT_PUBLIC_` for client-side access.

## Testing the Configuration

The configuration has been tested with:
- Next.js 16.1.1
- Turbopack
- Tailwind CSS v4
- TypeScript
- ES Modules
- React Server Components
- Client Components

All module imports and exports work correctly without format mismatch errors.