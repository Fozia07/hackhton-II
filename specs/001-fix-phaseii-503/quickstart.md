# Quickstart Guide: Phase II Authentication

**Date**: 2026-02-07
**Feature**: 001-fix-phaseii-503
**Phase**: Phase 1 Design
**Status**: Complete

## Overview

This guide provides step-by-step instructions for setting up, running, and deploying the Phase II authentication system. It covers both local development and production deployment.

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 20+ | Frontend runtime |
| PostgreSQL | 15+ | Database (or use Neon hosted) |
| Git | Latest | Version control |

### Optional Tools

- **curl** or **Postman**: API testing
- **jq**: JSON formatting for command line
- **Docker**: Containerized deployment (optional)

### Knowledge Requirements

- Basic understanding of REST APIs
- Familiarity with command line/terminal
- Understanding of environment variables

---

## Local Development Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd hackhton-II

# Navigate to Phase II directory
cd phaseII
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

#### 2.2 Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

#### 2.3 Configure Environment Variables

Create `.env` file in `phaseII/backend/`:

```bash
# Copy example file
cp .env.example .env

# Edit .env file
nano .env
```

**Required Environment Variables**:

```env
# Application Configuration
APP_TITLE=Phase 2 Backend
APP_VERSION=0.1.0
DEBUG=False

# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-generate-with-openssl
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3001,http://localhost:3002,https://hackhton-ii.vercel.app
```

**Generate JWT Secret Key**:
```bash
# Generate a secure random key
openssl rand -hex 32
```

**Database URL Format**:
```
postgresql+asyncpg://username:password@host:port/database

# Example for Neon PostgreSQL:
postgresql+asyncpg://neondb_owner:password@ep-xxx.region.aws.neon.tech/neondb
```

#### 2.4 Verify Backend Setup

```bash
# Test database connection
python -c "from app.core.database import engine; print('Database configured' if engine else 'Database not configured')"

# Run backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Expected Output**:
```
INFO:     Will watch for changes in these directories: ['C:\\...\\phaseII\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Database tables created successfully
INFO:     Application startup complete.
```

**Test Health Check**:
```bash
curl http://localhost:8001/health
```

**Expected Response**:
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2026-02-07T12:00:00Z"
}
```

---

### Step 3: Frontend Setup

#### 3.1 Install Dependencies

```bash
cd ../frontend

# Install Node.js dependencies
npm install
```

#### 3.2 Configure Environment Variables

Create `.env.local` file in `phaseII/frontend/`:

```bash
# Copy example file
cp .env.example .env.local

# Edit .env.local file
nano .env.local
```

**Required Environment Variables**:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_URL=http://localhost:3001

# Environment
NODE_ENV=development
```

**⚠️ CRITICAL**: Ensure `NEXT_PUBLIC_API_URL` points to your local backend (http://localhost:8001), NOT a remote URL.

#### 3.3 Verify Frontend Setup

```bash
# Run frontend
npm run dev
```

**Expected Output**:
```
▲ Next.js 16.1.1 (Turbopack)
- Local:        http://localhost:3001
- Network:      http://192.168.1.36:3001
- Environments: .env.local

✓ Starting...
✓ Ready in 1759ms
```

**Test Frontend**:
Open browser to http://localhost:3001

---

## Running the Application

### Start Both Services

**Terminal 1 - Backend**:
```bash
cd phaseII/backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend**:
```bash
cd phaseII/frontend
npm run dev
```

### Verify Services are Running

```bash
# Check backend
curl http://localhost:8001/health

# Check frontend (in browser)
# Open http://localhost:3001
```

---

## Testing Authentication

### Test Signup Flow

#### 1. Via Browser

1. Open http://localhost:3001/signup
2. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `SecurePass123!`
3. Click "Sign Up"
4. Verify redirect to dashboard

#### 2. Via curl

```bash
# Create new user
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected Response** (201 Created):
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2026-02-07T10:30:00Z",
  "updated_at": "2026-02-07T10:30:00Z",
  "is_active": true
}
```

---

### Test Signin Flow

#### 1. Via Browser

1. Open http://localhost:3001/login
2. Fill in the form:
   - Username: `testuser` (or `test@example.com`)
   - Password: `SecurePass123!`
3. Click "Sign In"
4. Verify redirect to dashboard

#### 2. Via curl

```bash
# Sign in
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "testuser"
}
```

#### 3. Use Token for Authenticated Request

```bash
# Get current user profile
TOKEN="<access_token_from_signin>"
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## Environment Configuration

### Development Environment

**Backend** (`phaseII/backend/.env`):
```env
APP_TITLE=Phase 2 Backend
APP_VERSION=0.1.0
DEBUG=True  # Enable debug mode for development
DATABASE_URL=postgresql+asyncpg://localhost:5432/phaseii_dev
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3001,http://localhost:3002
```

**Frontend** (`phaseII/frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_URL=http://localhost:3001
NODE_ENV=development
```

---

### Production Environment

**Backend** (`phaseII/backend/.env.production`):
```env
APP_TITLE=Phase 2 Backend
APP_VERSION=0.1.0
DEBUG=False  # Disable debug mode in production
DATABASE_URL=postgresql+asyncpg://user:pass@production-host:5432/phaseii_prod
JWT_SECRET_KEY=<generate-secure-key-with-openssl-rand-hex-32>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://hackhton-ii.vercel.app
```

**Frontend** (`phaseII/frontend/.env.production`):
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NEXT_PUBLIC_APP_URL=https://hackhton-ii.vercel.app
NODE_ENV=production
```

---

## Deployment

### Backend Deployment (Railway)

#### 1. Prepare for Deployment

```bash
cd phaseII/backend

# Ensure requirements.txt is up to date
pip freeze > requirements.txt

# Create Procfile (if not exists)
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

#### 2. Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set DATABASE_URL="postgresql+asyncpg://..."
railway variables set JWT_SECRET_KEY="<secure-key>"
railway variables set ALLOWED_ORIGINS="https://hackhton-ii.vercel.app"

# Deploy
railway up
```

#### 3. Verify Deployment

```bash
# Get deployment URL
railway domain

# Test health check
curl https://your-backend-url.railway.app/health
```

---

### Frontend Deployment (Vercel)

#### 1. Prepare for Deployment

```bash
cd phaseII/frontend

# Ensure dependencies are installed
npm install

# Test build locally
npm run build
```

#### 2. Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? hackhton-ii-phaseii
# - Directory? ./
# - Override settings? No
```

#### 3. Configure Environment Variables

```bash
# Add environment variables via Vercel CLI
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://your-backend-url.railway.app

vercel env add NEXT_PUBLIC_APP_URL production
# Enter: https://hackhton-ii.vercel.app

# Redeploy with new environment variables
vercel --prod
```

#### 4. Verify Deployment

Open https://hackhton-ii.vercel.app and test authentication flows.

---

## Troubleshooting

### Issue 1: Frontend Shows 503 Error

**Symptoms**:
- Frontend shows "503 Service Unavailable" error
- Backend logs show no incoming requests

**Root Cause**: Frontend is configured to call wrong backend URL

**Solution**:
1. Check `phaseII/frontend/.env.local`:
   ```bash
   cat phaseII/frontend/.env.local
   ```
2. Verify `NEXT_PUBLIC_API_URL=http://localhost:8001`
3. If incorrect, update the file:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > phaseII/frontend/.env.local
   echo "NEXT_PUBLIC_APP_URL=http://localhost:3001" >> phaseII/frontend/.env.local
   echo "NODE_ENV=development" >> phaseII/frontend/.env.local
   ```
4. Restart frontend:
   ```bash
   # Stop frontend (Ctrl+C)
   npm run dev
   ```
5. Clear browser cache and test again

---

### Issue 2: CORS Error in Browser

**Symptoms**:
- Browser console shows CORS error
- Request is blocked by CORS policy

**Root Cause**: Backend CORS configuration doesn't include frontend origin

**Solution**:
1. Check backend CORS configuration in `phaseII/backend/app/main.py`
2. Verify `ALLOWED_ORIGINS` in `.env` includes `http://localhost:3001`
3. Update `phaseII/backend/.env`:
   ```env
   ALLOWED_ORIGINS=http://localhost:3001,http://localhost:3002,https://hackhton-ii.vercel.app
   ```
4. Restart backend:
   ```bash
   # Stop backend (Ctrl+C)
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

---

### Issue 3: Database Connection Error

**Symptoms**:
- Backend fails to start
- Error: "Database connection failed"

**Root Cause**: Invalid DATABASE_URL or database not accessible

**Solution**:
1. Verify DATABASE_URL format:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@host:port/database
   ```
2. Test database connectivity:
   ```bash
   # Using psql
   psql "postgresql://username:password@host:port/database"
   ```
3. For Neon PostgreSQL, ensure SSL is enabled:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/db?sslmode=require
   ```
4. Check firewall rules allow connection to database

---

### Issue 4: JWT Token Invalid

**Symptoms**:
- Authenticated requests return 401 Unauthorized
- Error: "Could not validate credentials"

**Root Cause**: JWT_SECRET_KEY mismatch or token expired

**Solution**:
1. Verify JWT_SECRET_KEY is set in backend `.env`
2. Ensure JWT_SECRET_KEY hasn't changed (invalidates all existing tokens)
3. Check token expiration (default 30 minutes)
4. Sign in again to get new token

---

### Issue 5: Port Already in Use

**Symptoms**:
- Error: "Address already in use"
- Backend or frontend fails to start

**Solution**:

**For Backend (Port 8001)**:
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8001 | xargs kill -9
```

**For Frontend (Port 3001)**:
```bash
# Windows
netstat -ano | findstr :3001
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3001 | xargs kill -9
```

---

### Issue 6: Module Not Found Error

**Symptoms**:
- Backend: "ModuleNotFoundError: No module named 'fastapi'"
- Frontend: "Cannot find module 'next'"

**Solution**:

**Backend**:
```bash
cd phaseII/backend
source .venv/bin/activate
pip install -r requirements.txt
```

**Frontend**:
```bash
cd phaseII/frontend
npm install
```

---

## Request Logging

### Enable Request Logging (Recommended for Development)

Add middleware to `phaseII/backend/app/main.py`:

```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log incoming request
    logger.info(f"→ {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Log response
    duration = (time.time() - start_time) * 1000
    logger.info(f"← {request.method} {request.url.path} {response.status_code} {duration:.2f}ms")

    return response
```

**Example Output**:
```
INFO: → POST /auth/signup
INFO: ← POST /auth/signup 201 245.32ms
INFO: → POST /auth/signin
INFO: ← POST /auth/signin 200 189.45ms
```

---

## Development Workflow

### Daily Development

1. **Start Services**:
   ```bash
   # Terminal 1: Backend
   cd phaseII/backend && source .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

   # Terminal 2: Frontend
   cd phaseII/frontend && npm run dev
   ```

2. **Make Changes**: Edit code in your IDE

3. **Test Changes**: Services auto-reload on file changes

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: description of changes"
   git push
   ```

---

### Testing Checklist

Before committing changes, verify:

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Health check returns 200 OK
- [ ] Signup flow works (create new user)
- [ ] Signin flow works (authenticate user)
- [ ] Authenticated requests work (use token)
- [ ] Error handling works (invalid credentials, duplicate user)
- [ ] CORS works (no browser console errors)

---

## Performance Monitoring

### Monitor Backend Performance

```bash
# Check response times
curl -w "\nTime: %{time_total}s\n" http://localhost:8001/health

# Monitor logs
tail -f logs/app.log  # if logging to file

# Check database latency
curl http://localhost:8001/health | jq '.database.latency_ms'
```

### Monitor Frontend Performance

Open browser DevTools:
- Network tab: Check request/response times
- Console tab: Check for errors
- Performance tab: Analyze page load time

---

## Security Checklist

### Development

- [ ] Use `.env` files for sensitive configuration
- [ ] Never commit `.env` files to git (add to `.gitignore`)
- [ ] Use strong JWT secret key (generate with `openssl rand -hex 32`)
- [ ] Enable CORS only for trusted origins

### Production

- [ ] Use HTTPS for all communication
- [ ] Use strong, unique JWT secret key
- [ ] Set `DEBUG=False` in backend
- [ ] Restrict CORS to production frontend URL only
- [ ] Use environment variables for all secrets
- [ ] Enable database SSL connection
- [ ] Implement rate limiting
- [ ] Monitor failed authentication attempts
- [ ] Regular security updates for dependencies

---

## Additional Resources

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [JWT.io](https://jwt.io/) - JWT debugger

### API Documentation

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Support

- **Issues**: Report bugs at [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: Ask questions at [GitHub Discussions](https://github.com/your-repo/discussions)

---

## Summary

### Quick Commands Reference

```bash
# Backend
cd phaseII/backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Frontend
cd phaseII/frontend
npm run dev

# Test health check
curl http://localhost:8001/health

# Test signup
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"SecurePass123!"}'

# Test signin
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"SecurePass123!"}'
```

---

**Quickstart Guide Complete** ✅

You should now be able to set up, run, and deploy the Phase II authentication system successfully.
