/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Include better-auth in server external packages for Vercel deployment
  serverExternalPackages: [
    "better-auth", // Include better-auth in server external packages
  ],
  // Allow importing from src directory
  outputFileTracingRoot: process.cwd(),
};

export default nextConfig;