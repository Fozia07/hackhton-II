// src/lib/auth/index.ts
import { betterAuth } from 'better-auth';
import { nextJs } from 'better-auth/next-js';

export const auth = betterAuth({
  database: {
    provider: 'sqlite', // or 'postgresql', 'mysql'
    url: process.env.DATABASE_URL!,
  },
  secret: process.env.BETTER_AUTH_SECRET || 'your-secret-key-here',
  trustHost: true,
  // Add any additional configuration here
});

export const { GET, POST } = nextJs(auth);