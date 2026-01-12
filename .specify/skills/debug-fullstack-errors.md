# Generic Full-Stack Error Debugging Skill

**Skill Name:** `debug-fullstack-errors`
**Type:** Systematic Error Diagnosis
**Applicable To:** Any JWT + Next.js + FastAPI project
**Mode:** Code Analysis Only (No Web Search)

---

## Skill Purpose

Systematically diagnose and fix common full-stack authentication and routing errors in web applications using:
- JWT authentication
- Next.js frontend
- FastAPI backend
- CORS issues
- API communication failures

---

## Core Principles

1. **No Assumptions** - Verify everything, assume nothing
2. **Step-by-Step** - Follow systematic debugging flow
3. **Root Cause First** - Find the real problem, not symptoms
4. **Actionable Fixes** - Provide exact code changes, not theory
5. **Fast Iteration** - Prioritize quick fixes for time-sensitive projects

---

## Error Categories

### Category A: Network & Communication Errors
- "Failed to fetch"
- CORS policy blocked
- Network request failed
- Connection refused
- Timeout errors

### Category B: Authentication Errors
- 401 Unauthorized
- 403 Forbidden
- Invalid token
- Token expired
- Missing authorization header

### Category C: Routing Errors
- 404 Not Found (pages)
- 404 Not Found (API endpoints)
- Redirect loops
- Protected route access denied

### Category D: Type & Import Errors
- Module not found
- Type errors
- Import path errors
- Missing dependencies

---

## Systematic Debugging Flow

### Phase 1: Verify Backend Accessibility

**Goal:** Confirm backend is running and reachable

**Steps:**
1. Check if backend process is running
2. Test health/ping endpoint
3. Verify correct port
4. Check firewall/antivirus blocking

**Commands:**
```bash
# Test backend health
curl -X GET http://localhost:PORT/health

# Check if port is in use
netstat -ano | findstr :PORT

# Test API docs endpoint
curl -I http://localhost:PORT/docs
```

**Expected:** 200 OK responses
**If Failed:** Backend not running or wrong port

---

### Phase 2: Validate API Configuration

**Goal:** Ensure frontend knows where backend is

**Check:**
1. Environment variables for API URL
2. Service/client files using API URL
3. Protocol (http vs https)
4. Port numbers match
5. No trailing slashes

**Common Patterns:**
```typescript
// Environment variable
NEXT_PUBLIC_API_URL=http://localhost:8000

// In service file
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

**Common Mistakes:**
- Using `127.0.0.1` instead of `localhost`
- Wrong port number
- Missing `http://` protocol
- Trailing slash causing double slashes

---

### Phase 3: CORS Configuration Check

**Goal:** Ensure backend allows frontend requests

**Backend Requirements:**
```python
# FastAPI CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Environment Configuration:**
```bash
# In backend .env file
ALLOWED_ORIGINS=*
# OR
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Critical:** Backend must be restarted after CORS changes

**Browser Console Check:**
Look for: `Access to fetch at 'http://...' from origin 'http://...' has been blocked by CORS policy`

---

### Phase 4: Request Structure Validation

**Goal:** Verify API requests are properly formatted

**Check:**
1. HTTP method (GET, POST, PUT, DELETE)
2. Headers (Content-Type, Authorization)
3. Request body structure
4. JSON stringification

**Correct Pattern:**
```typescript
const response = await fetch(`${API_URL}/endpoint`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,  // If authenticated
  },
  body: JSON.stringify(data),  // Must stringify
});
```

**Common Mistakes:**
- Missing `Content-Type: application/json`
- Not stringifying request body
- Wrong HTTP method
- Malformed JSON

---

### Phase 5: JWT Token Lifecycle

**Goal:** Verify token is received, stored, and sent correctly

**A) Token Generation (Backend)**
```python
# Must return access_token
return {
    "access_token": token,
    "token_type": "bearer",
    # ... other data
}
```

**B) Token Storage (Frontend)**
```typescript
// After successful login/signup
const authData = await response.json();
localStorage.setItem('auth_token', authData.access_token);
```

**C) Token Retrieval & Usage**
```typescript
// In protected requests
const token = localStorage.getItem('auth_token');
headers: {
  'Authorization': `Bearer ${token}`,  // MUST have "Bearer " prefix
}
```

**Verification Checklist:**
- [ ] Token received in login/signup response?
- [ ] Token stored in localStorage?
- [ ] Token retrieved before protected requests?
- [ ] Token sent with "Bearer " prefix?
- [ ] Token not expired?

---

### Phase 6: Route Configuration

**Goal:** Verify routes exist and are accessible

**Next.js App Router Structure:**
```
app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   └── signup/
│       └── page.tsx
├── (dashboard)/
│   ├── layout.tsx
│   └── page.tsx
└── layout.tsx
```

**Key Points:**
- Route groups `(name)` don't affect URL
- `page.tsx` is required for routes
- `layout.tsx` wraps child routes
- Case-sensitive on Linux/Mac

**Backend Route Mounting:**
```python
# Routes must be included
app.include_router(auth_router)
app.include_router(todos_router)
```

---

### Phase 7: Protected Route Logic

**Goal:** Ensure authentication checks work correctly

**Pattern:**
```typescript
export function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return <>{children}</>;
}
```

**Common Issues:**
- Infinite redirect loops
- Not checking loading state
- Wrong redirect path
- Not wrapping protected pages

---

### Phase 8: Type & Import Resolution

**Goal:** Fix TypeScript and import errors

**Check:**
1. Type definition files exist
2. Import paths are correct
3. Types match between frontend/backend
4. No circular dependencies

**Common Patterns:**
```typescript
// Relative import
import { User } from '../types/auth';

// Alias import (if configured)
import { User } from '@/types/auth';

// Type definition
export interface User {
  id: number;
  username: string;
  email: string;
  // ... other fields
}
```

---

## Error Diagnosis Matrix

### Error: "Failed to fetch"

**Possible Causes:**
1. Backend not running
2. Wrong API URL
3. CORS blocking
4. Network/firewall issue
5. Invalid request format

**Diagnosis Steps:**
1. Test backend directly with curl
2. Check browser Network tab
3. Verify API URL in code
4. Check CORS configuration
5. Inspect request headers/body

---

### Error: CORS Policy Blocked

**Possible Causes:**
1. CORS middleware not configured
2. Wrong origin in allowed list
3. Backend not restarted after config change
4. Credentials mode mismatch

**Diagnosis Steps:**
1. Check CORS middleware exists
2. Verify allowed origins include frontend
3. Restart backend
4. Clear browser cache
5. Test with curl including Origin header

---

### Error: 401 Unauthorized

**Possible Causes:**
1. Token not sent
2. Token expired
3. Wrong token format
4. Invalid token
5. Backend JWT verification failed

**Diagnosis Steps:**
1. Check token exists in localStorage
2. Verify token sent in Authorization header
3. Check "Bearer " prefix present
4. Decode JWT to check expiration
5. Verify backend JWT secret matches

---

### Error: 404 Not Found (Page)

**Possible Causes:**
1. Page file doesn't exist
2. Wrong file location
3. Incorrect file naming
4. Route group misconfiguration
5. Case sensitivity issue

**Diagnosis Steps:**
1. Verify page.tsx exists at correct path
2. Check route group parentheses
3. Verify file naming (page.tsx not Page.tsx)
4. Check Next.js routing structure
5. Restart dev server

---

### Error: 404 Not Found (API)

**Possible Causes:**
1. Route not registered
2. Wrong endpoint path
3. HTTP method mismatch
4. Router not included in app

**Diagnosis Steps:**
1. Check backend route definition
2. Verify router is included in main app
3. Test endpoint with curl
4. Check API documentation
5. Verify HTTP method matches

---

### Error: Type/Import Errors

**Possible Causes:**
1. Type file doesn't exist
2. Wrong import path
3. Type mismatch
4. Missing type definition
5. Circular dependency

**Diagnosis Steps:**
1. Verify type file exists
2. Check import path (relative vs alias)
3. Verify type definitions match usage
4. Check for circular imports
5. Restart TypeScript server

---

## Output Format Template

When diagnosing an error, use this format:

```markdown
### 🔍 Root Cause
[One sentence describing the exact problem]

### 🧩 Why This Happened
[2-3 sentences explaining the technical reason]

### ✅ Fix

**File:** `path/to/file`

```language
// Code fix here
```

**Steps:**
1. [Action 1]
2. [Action 2]
3. [Restart/refresh if needed]

### 🧪 Verify Fix

```bash
# Command to test
```

**Expected:** [What should happen]
```

---

## Quick Reference: Common Fixes

### Fix: CORS Error
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
**Action:** Restart backend

---

### Fix: Token Not Sent
```typescript
// Add to request headers
headers: {
  'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
  'Content-Type': 'application/json',
}
```

---

### Fix: Wrong API URL
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```
**Action:** Restart frontend

---

### Fix: 404 Dashboard
```
# Verify file exists at:
app/(dashboard)/page.tsx
# OR
app/dashboard/page.tsx
```

---

### Fix: Import Error
```typescript
// Check type file exists
// types/auth.ts

// Use correct import
import { User } from '@/types/auth';
// OR
import { User } from '../types/auth';
```

---

## Debugging Checklist

Before asking for help, verify:

- [ ] Backend is running and accessible
- [ ] Frontend environment variables are correct
- [ ] CORS is configured and backend restarted
- [ ] API requests have correct headers
- [ ] JWT token is stored and sent correctly
- [ ] Routes exist at correct file paths
- [ ] Type definitions exist and imports are correct
- [ ] Browser console shows exact error
- [ ] Network tab shows request/response details

---

## Usage Instructions

1. **Identify Error Category** (Network, Auth, Routing, Type)
2. **Follow Relevant Phase** in debugging flow
3. **Use Diagnosis Matrix** for specific error
4. **Apply Fix** using output format
5. **Verify** fix worked

---

## Skill Invocation Example

**Input:**
```
Error: Failed to fetch
Context: Signup form submission
Browser: CORS policy blocked
Frontend: localhost:3009
Backend: localhost:8000
```

**Output:**

### 🔍 Root Cause
CORS middleware not allowing requests from frontend origin

### 🧩 Why This Happened
The backend CORS configuration doesn't include the frontend's origin (localhost:3009) in the allowed origins list, causing the browser to block the request.

### ✅ Fix

**File:** `backend/.env`

```bash
ALLOWED_ORIGINS=*
```

**File:** `backend/main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Steps:**
1. Update .env file with ALLOWED_ORIGINS=*
2. Verify CORS middleware is added in main.py
3. Restart backend server
4. Clear browser cache or use incognito
5. Try signup again

### 🧪 Verify Fix

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3009" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'
```

**Expected:** Should return success response without CORS error

---

## Maintenance

Update this skill when:
- New error patterns emerge
- Framework versions change
- New debugging techniques discovered
- Common fixes evolve

**Version:** 1.0
**Last Updated:** 2026-01-10
**Applicable To:** JWT + Next.js + FastAPI projects
