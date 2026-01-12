/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Allow importing from src directory
  outputFileTracingRoot: process.cwd(),
};

export default nextConfig;