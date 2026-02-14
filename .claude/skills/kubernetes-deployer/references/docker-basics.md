# Docker Basics

Comprehensive guide to creating optimized Dockerfiles for Kubernetes deployments.

## Table of Contents

- [Dockerfile Fundamentals](#dockerfile-fundamentals)
- [Multi-Stage Builds](#multi-stage-builds)
- [Language-Specific Patterns](#language-specific-patterns)
- [Optimization Techniques](#optimization-techniques)
- [Security Best Practices](#security-best-practices)
- [Common Pitfalls](#common-pitfalls)

---

## Dockerfile Fundamentals

### Basic Structure

```dockerfile
# Base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Set user (security)
USER node

# Start command
CMD ["node", "server.js"]
```

### Key Instructions

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Base image | `FROM node:20-alpine` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host | `COPY . .` |
| `RUN` | Execute commands | `RUN npm install` |
| `ENV` | Set environment variables | `ENV NODE_ENV=production` |
| `EXPOSE` | Document port | `EXPOSE 3000` |
| `USER` | Set user context | `USER node` |
| `CMD` | Default command | `CMD ["node", "app.js"]` |
| `ENTRYPOINT` | Fixed command | `ENTRYPOINT ["docker-entrypoint.sh"]` |

---

## Multi-Stage Builds

### Why Multi-Stage?

- **Smaller images**: Remove build tools from final image
- **Faster deployments**: Less data to transfer
- **Better security**: Fewer attack surfaces
- **Cleaner separation**: Build vs runtime dependencies

### Node.js Multi-Stage

```dockerfile
# Stage 1: Build
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production

# Stage 2: Runtime
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
USER node
CMD ["node", "dist/index.js"]
```

### Python Multi-Stage

```dockerfile
# Stage 1: Build
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go Multi-Stage

```dockerfile
# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Runtime
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

### Java Multi-Stage

```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## Language-Specific Patterns

### Node.js / TypeScript

**Development:**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
```

**Production:**
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
ENV NODE_ENV=production
EXPOSE 3000
USER node
CMD ["node", "dist/server.js"]
```

### Python / FastAPI

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o main .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/main /main
EXPOSE 8080
ENTRYPOINT ["/main"]
```

### Rust

```dockerfile
FROM rust:1.75 AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src
COPY src ./src
RUN touch src/main.rs
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp
EXPOSE 8080
CMD ["myapp"]
```

---

## Optimization Techniques

### 1. Layer Caching

**Bad (cache invalidated on any file change):**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install
```

**Good (cache dependencies separately):**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
```

### 2. Minimize Layers

**Bad (multiple RUN commands):**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean
```

**Good (combine commands):**
```dockerfile
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Use .dockerignore

Create `.dockerignore`:
```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.local
*.md
.vscode
.idea
dist
build
coverage
.DS_Store
```

### 4. Choose Minimal Base Images

| Image Type | Size | Use Case |
|------------|------|----------|
| `node:20` | ~1GB | Development |
| `node:20-slim` | ~200MB | Production with native deps |
| `node:20-alpine` | ~120MB | Production (recommended) |
| `scratch` | ~0MB | Static binaries only |

### 5. Remove Build Dependencies

```dockerfile
FROM python:3.11-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*
```

### 6. Use Specific Tags

**Bad:**
```dockerfile
FROM node:latest  # Unpredictable
```

**Good:**
```dockerfile
FROM node:20.11.0-alpine3.19  # Reproducible
```

---

## Security Best Practices

### 1. Run as Non-Root User

```dockerfile
FROM node:20-alpine

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app
COPY --chown=nodejs:nodejs . .

USER nodejs
CMD ["node", "server.js"]
```

### 2. Scan for Vulnerabilities

```bash
# Using Docker Scout
docker scout cves myapp:latest

# Using Trivy
trivy image myapp:latest

# Using Snyk
snyk container test myapp:latest
```

### 3. Use Secrets Properly

**Bad (secrets in image):**
```dockerfile
ENV API_KEY=secret123  # Never do this!
```

**Good (secrets at runtime):**
```dockerfile
# No secrets in Dockerfile
# Pass via Kubernetes Secrets
```

### 4. Minimize Attack Surface

```dockerfile
# Remove unnecessary packages
RUN apk del build-dependencies

# Remove shell access (for Go/Rust)
FROM scratch
COPY --from=builder /app/binary /binary
ENTRYPOINT ["/binary"]
```

### 5. Keep Images Updated

```dockerfile
# Pin versions but update regularly
FROM node:20.11.0-alpine3.19

# Update base packages
RUN apk update && apk upgrade
```

---

## Common Pitfalls

### 1. Large Image Sizes

**Problem:**
```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y nodejs npm
COPY . .
```

**Solution:**
```dockerfile
FROM node:20-alpine
COPY package*.json ./
RUN npm ci --only=production
COPY . .
```

### 2. Cache Invalidation

**Problem:**
```dockerfile
COPY . .
RUN npm install  # Runs every time any file changes
```

**Solution:**
```dockerfile
COPY package*.json ./
RUN npm ci
COPY . .  # Only invalidates after dependency changes
```

### 3. Running as Root

**Problem:**
```dockerfile
FROM node:20-alpine
COPY . .
CMD ["node", "app.js"]  # Runs as root
```

**Solution:**
```dockerfile
FROM node:20-alpine
COPY . .
USER node
CMD ["node", "app.js"]
```

### 4. Hardcoded Configuration

**Problem:**
```dockerfile
ENV DATABASE_URL=postgresql://localhost:5432/db
```

**Solution:**
```dockerfile
# No hardcoded values
# Use Kubernetes ConfigMaps/Secrets
```

### 5. Missing Health Checks

**Problem:**
```dockerfile
# No health check defined
```

**Solution:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1
```

---

## Build Commands

### Basic Build

```bash
docker build -t myapp:latest .
```

### Build with Arguments

```dockerfile
ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-alpine
```

```bash
docker build --build-arg NODE_VERSION=18 -t myapp:latest .
```

### Multi-Platform Build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

### Build with Cache

```bash
# Use cache from registry
docker build --cache-from myapp:latest -t myapp:v2 .

# Use BuildKit cache
docker buildx build --cache-from type=registry,ref=myapp:cache \
  --cache-to type=registry,ref=myapp:cache,mode=max \
  -t myapp:latest .
```

---

## Testing Images

### Test Locally

```bash
# Run container
docker run -p 3000:3000 myapp:latest

# Run with environment variables
docker run -e NODE_ENV=production -p 3000:3000 myapp:latest

# Run interactively
docker run -it myapp:latest /bin/sh

# Check logs
docker logs <container-id>
```

### Inspect Image

```bash
# View image layers
docker history myapp:latest

# Inspect image details
docker inspect myapp:latest

# Check image size
docker images myapp:latest
```

### Dive Tool

```bash
# Install dive
brew install dive

# Analyze image
dive myapp:latest
```

---

## Complete Example: Production-Ready Node.js

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build && \
    npm prune --production

# Stage 3: Runtime
FROM node:20-alpine AS runner
WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built application
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs package.json ./

# Set environment
ENV NODE_ENV=production
ENV PORT=3000

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/server.js"]
```

Build and test:
```bash
# Build
docker build -t myapp:latest .

# Test
docker run -p 3000:3000 myapp:latest

# Check size
docker images myapp:latest

# Scan for vulnerabilities
docker scout cves myapp:latest
```
