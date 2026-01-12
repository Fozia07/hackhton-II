# Quickstart Guide: Auth Integration Fix

## Prerequisites

- Node.js 18+ installed
- Python 3.9+ installed
- PostgreSQL or Neon database access
- Git installed

## Setup Instructions

### 1. Backend Setup

1. Navigate to backend directory:
```bash
cd phaseII/backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Update environment variables in `.env`:
```bash
# Ensure CORS is configured properly
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3007,http://localhost:3009
```

4. Start the backend server:
```bash
python -m uvicorn app.main:app --reload --host localhost --port 8000
```

### 2. Frontend Setup

1. Navigate to frontend directory:
```bash
cd phaseII/frontend
```

2. Install JavaScript dependencies:
```bash
npm install
```

3. Verify environment variables in `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3007
```

4. Start the frontend server:
```bash
npm run dev
```

## Verification Steps

### 1. Test Authentication Flow

1. Open browser to frontend URL (e.g., http://localhost:3007)
2. Navigate to signup page
3. Create a new account
4. Verify account creation succeeds without "Failed to fetch" errors
5. Login with created credentials
6. Verify login succeeds and redirects properly

### 2. Test Dashboard Access

1. After successful login, navigate to dashboard
2. Verify dashboard loads without 404 errors
3. Verify user session is maintained

### 3. Test Todo Functionality

1. On dashboard, create a new todo
2. Verify todo creation succeeds
3. Update and delete todos
4. Verify all Todo API endpoints work correctly

## Common Issues & Solutions

### Issue: "Failed to fetch" errors
**Cause**: CORS misconfiguration
**Solution**: Update `ALLOWED_ORIGINS` in backend `.env` file

### Issue: Dashboard 404 after login
**Cause**: ProtectedRoute logic issue
**Solution**: Check AuthContext implementation and authentication state checking

### Issue: AuthContext import errors
**Cause**: Missing or incorrect type import
**Solution**: Verify `types/auth.ts` file exists with proper User interface

## API Endpoints

### Authentication Endpoints
- `POST /auth/signup` - Create new user
- `POST /auth/signin` - Authenticate user
- `GET /auth/me` - Get user profile

### Todo Endpoints
- `GET /todos` - Get user's todos
- `POST /todos` - Create new todo
- `PUT /todos/{id}` - Update todo
- `DELETE /tos/{id}` - Delete todo

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - Database connection string
- `JWT_SECRET_KEY` - Secret for JWT signing
- `ALLOWED_ORIGINS` - Origins allowed for CORS

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_APP_URL` - Frontend app URL