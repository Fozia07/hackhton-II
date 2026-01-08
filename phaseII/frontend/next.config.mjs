/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Configure for Turbopack root directory to resolve workspace detection
  // This tells Next.js which directory to treat as the workspace root
  // to avoid confusion with multiple lockfiles
  turbopack: {
    root: process.cwd(), // Explicitly set the root to current working directory
  },
  // Use serverExternalPackages instead of the experimental option
  serverExternalPackages: [],
};

export default nextConfig;