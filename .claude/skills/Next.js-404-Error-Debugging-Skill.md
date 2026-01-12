# Next.js 404 Error Debugging Skill

## Overview
This skill helps diagnose and fix "404 - This page could not be found" errors in Next.js applications.

## Quick Diagnosis Checklist

### 1. Identify Router Type
```bash
# Check if using App Router or Pages Router
ls -la app/     # App Router (Next.js 13+)
ls -la pages/   # Pages Router (Next.js 12 and below)
```

### 2. Common Causes

#### App Router (Next.js 13+)
- ✅ Correct: `app/dashboard/page.tsx`
- ❌ Wrong: `app/dashboard.tsx`
- ❌ Wrong: `app/dashboard/index.tsx`
- ⚠️ Route Groups: `app/(dashboard)/page.tsx` → URL is `/` not `/dashboard`

#### Pages Router (Next.js 12-)
- ✅ Correct: `pages/dashboard.tsx`
- ✅ Correct: `pages/dashboard/index.tsx`
- ❌ Wrong: `pages/dashboard/dashboard.tsx`

## Step-by-Step Fix Process

### For App Router

#### Step 1: Check File Structure
```bash
# List all route files
find app -name "page.tsx" -o -name "page.js"

# Check for route groups (folders with parentheses)
ls -la app/ | grep "("
```

#### Step 2: Identify Route Group Issue
If you see `(dashboard)` or any folder with parentheses:

**Problem**: Route groups don't appear in URLs
- `app/(dashboard)/page.tsx` → accessible at `/` (root)
- `app/(auth)/login/page.tsx` → accessible at `/login`

**Solution**: Remove parentheses if you want the folder name in URL
```bash
# Rename route group to regular folder
mv app/\(dashboard\) app/dashboard

# Or on Windows
move "app/(dashboard)" "app/dashboard"
```

#### Step 3: Verify File Naming
```bash
# File MUST be named exactly "page.tsx" or "page.js"
# Check your dashboard file
ls -la app/dashboard/

# Should see:
# page.tsx (or page.js)
# NOT: dashboard.tsx, index.tsx, Dashboard.tsx
```

#### Step 4: Verify Export Statement
```bash
# Check if page has default export
grep -n "export default" app/dashboard/page.tsx

# Should see something like:
# export default function Dashboard()
# or
# export default async function Dashboard()
```

#### Step 5: Restart Dev Server
```bash
# Always restart after route changes
# Press Ctrl+C to stop, then:
npm run dev
# or
yarn dev
# or
pnpm dev
```

### For Pages Router

#### Step 1: Check File Location
```bash
# List all route files
ls -la pages/

# Your dashboard should be:
# pages/dashboard.tsx (for /dashboard)
# or
# pages/dashboard/index.tsx (for /dashboard)
```

#### Step 2: Verify Export
```bash
# Check for default export
grep -n "export default" pages/dashboard.tsx
```

#### Step 3: Restart Dev Server
```bash
npm run dev
```

## Common Patterns and Solutions

### Pattern 1: Route Group Confusion
**Symptom**: File exists at `app/(dashboard)/page.tsx` but `/dashboard` gives 404

**Diagnosis**:
```bash
ls -la app/ | grep "dashboard"
# If you see "(dashboard)", that's your issue
```

**Fix**:
```bash
# Remove parentheses from folder name
mv app/\(dashboard\) app/dashboard
npm run dev
```

### Pattern 2: Wrong File Name
**Symptom**: File exists at `app/dashboard/dashboard.tsx` but gives 404

**Diagnosis**:
```bash
ls -la app/dashboard/
# Should see "page.tsx" not "dashboard.tsx"
```

**Fix**:
```bash
mv app/dashboard/dashboard.tsx app/dashboard/page.tsx
npm run dev
```

### Pattern 3: Missing Default Export
**Symptom**: File exists with correct name but still 404

**Diagnosis**:
```bash
cat app/dashboard/page.tsx | grep "export"
# Should have "export default"
```

**Fix**: Add default export to the file
```typescript
// Ensure this exists in page.tsx
export default function Dashboard() {
  return <div>Dashboard</div>
}
```

### Pattern 4: TypeScript Extension Mismatch
**Symptom**: Using TypeScript but file is `.js` instead of `.tsx`

**Fix**:
```bash
mv app/dashboard/page.js app/dashboard/page.tsx
npm run dev
```

## Automated Diagnosis Script

Save this as `scripts/check-routes.js`:

```javascript
const fs = require('fs');
const path = require('path');

function checkRoutes() {
  console.log('🔍 Next.js Route Checker\n');
  
  // Check router type
  const hasAppDir = fs.existsSync('app');
  const hasPagesDir = fs.existsSync('pages');
  
  console.log('📂 Router Type:');
  if (hasAppDir) console.log('  ✓ App Router detected (app/ folder)');
  if (hasPagesDir) console.log('  ✓ Pages Router detected (pages/ folder)');
  console.log('');
  
  if (hasAppDir) {
    checkAppRouter();
  }
  
  if (hasPagesDir) {
    checkPagesRouter();
  }
}

function checkAppRouter() {
  console.log('📍 App Router Routes:\n');
  
  function scanDir(dir, basePath = '') {
    const items = fs.readdirSync(dir);
    
    items.forEach(item => {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        // Check for route groups
        const isRouteGroup = item.startsWith('(') && item.endsWith(')');
        const urlSegment = isRouteGroup ? '' : `/${item}`;
        
        if (isRouteGroup) {
          console.log(`  ⚠️  Route Group: ${item} (not in URL)`);
        }
        
        scanDir(fullPath, basePath + urlSegment);
      } else if (item === 'page.tsx' || item === 'page.js') {
        const url = basePath || '/';
        console.log(`  ✓ ${url.padEnd(30)} → ${fullPath}`);
      }
    });
  }
  
  scanDir('app');
  console.log('');
}

function checkPagesRouter() {
  console.log('📍 Pages Router Routes:\n');
  
  function scanDir(dir, basePath = '') {
    const items = fs.readdirSync(dir);
    
    items.forEach(item => {
      // Skip Next.js special files
      if (item.startsWith('_') || item === 'api') return;
      
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        scanDir(fullPath, basePath + `/${item}`);
      } else if (item.endsWith('.tsx') || item.endsWith('.js')) {
        const fileName = item.replace(/\.(tsx|js)$/, '');
        const url = fileName === 'index' 
          ? (basePath || '/') 
          : `${basePath}/${fileName}`;
        console.log(`  ✓ ${url.padEnd(30)} → ${fullPath}`);
      }
    });
  }
  
  scanDir('pages');
  console.log('');
}

checkRoutes();
```

**Usage**:
```bash
node scripts/check-routes.js
```

## Quick Reference Commands

```bash
# Check current routes
find app -name "page.tsx" -o -name "page.js"

# Find route groups
find app -type d -name "(*)"

# Check for default exports
grep -r "export default" app/*/page.tsx

# Rename route group
mv app/\(dashboard\) app/dashboard

# Restart dev server
npm run dev
```

## Prevention Tips

1. **Always use correct file names**:
   - App Router: `page.tsx` or `page.js`
   - Pages Router: `[name].tsx` or `index.tsx`

2. **Understand route groups**:
   - Use `(name)` only for organization, not URLs
   - Use `name` for actual URL paths

3. **Always restart after route changes**:
   - New routes require dev server restart
   - Hot reload doesn't always catch route changes

4. **Use TypeScript consistently**:
   - If project is TypeScript, use `.tsx` not `.js`

## Troubleshooting Flow

```
404 Error
    ↓
Does file exist at correct path?
    ├─ No → Create file at correct location
    └─ Yes → Check file name
        ├─ Wrong name → Rename to page.tsx
        └─ Correct → Check for route groups
            ├─ Has (parentheses) → Remove if URL needed
            └─ No parentheses → Check default export
                ├─ Missing → Add export default
                └─ Has export → Restart dev server
                    ├─ Still 404 → Check URL matches path
                    └─ Works → ✓ Fixed!
```

## Common Mistakes to Avoid

1. ❌ Creating `app/dashboard.tsx` instead of `app/dashboard/page.tsx`
2. ❌ Not restarting dev server after adding routes
3. ❌ Using route groups `(name)` when you want `name` in URL
4. ❌ Forgetting `export default` in page component
5. ❌ Mixing `.js` and `.tsx` extensions inconsistently
6. ❌ Creating `index.tsx` in App Router (use `page.tsx` instead)

## When to Use This Skill

- ✓ Getting "404 - This page could not be found" error
- ✓ Route works in development but not after deployment
- ✓ Authenticated users getting 404 on protected routes
- ✓ New route not appearing even after creation
- ✓ Confusion about route groups and URLs
- ✓ Migration from Pages Router to App Router