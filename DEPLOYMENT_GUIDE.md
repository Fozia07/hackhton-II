# Deployment Guide

## Deploying Backend to Railway

1. **Sign up for Railway** (if you haven't already):
   - Go to https://railway.app
   - Sign in with your GitHub account

2. **Prepare for Deployment**:
   - Make sure you've committed all changes to your repository
   - The backend is in `phaseII/backend/`

3. **Deploy Backend to Railway**:
   - In your Railway dashboard, click "New Project"
   - Select "GitHub" and choose your `hackhton-II` repository
   - Choose the branch where your backend code is (likely main or 018-fix-dashboard-404)
   - Railway will automatically detect this as a Python project

4. **Configure Environment Variables**:
   After the initial deployment, go to your Railway project settings and add these variables:

   - `JWT_SECRET_KEY`: Generate a secure secret key (at least 32 random characters)
   - `DATABASE_URL`: Railway will automatically provision a PostgreSQL database when you add the Database plugin

5. **Add a Database**:
   - In your Railway project, go to the "Plugins" tab
   - Click "Add Plugin" and select "PostgreSQL"
   - Railway will automatically connect it to your backend

6. **Redeploy**:
   - After adding environment variables and the database, click "Deploy" to redeploy with the new settings

## Deploying Frontend to Vercel

1. **Prepare for Deployment**:
   - The frontend is in `phaseII/frontend/`
   - Make sure your `.env.production` file is properly configured

2. **Deploy to Vercel**:
   - Go to https://vercel.com
   - Sign in with your GitHub account
   - Click "New Project" and import your `hackhton-II` repository
   - Vercel will automatically detect this as a Next.js project

3. **Configure Environment Variables in Vercel**:
   In your Vercel project settings, add:
   - `NEXT_PUBLIC_API_URL`: Your Railway backend URL (e.g., `https://your-project-id-production.up.railway.app`)
   - `NEXT_PUBLIC_APP_URL`: Your Vercel frontend URL (e.g., `https://hackhton-ii.vercel.app`)

4. **Deployment Settings**:
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Root Directory: `phaseII/frontend`

## Post-Deployment Steps

1. **Test CORS Connection**:
   - Visit your Vercel frontend URL
   - Try signing up/log in to ensure API calls work
   - Check browser developer tools to confirm no CORS errors

2. **Verify Database Connection**:
   - Create a test user account
   - Verify that data is being stored in your Railway PostgreSQL database

3. **Security Best Practices**:
   - Keep your JWT_SECRET_KEY secure
   - Regularly rotate your secret keys
   - Monitor your application logs for any suspicious activity

## Troubleshooting

### Common Issues:

1. **CORS Errors Persist**:
   - Verify that your Railway backend allows your Vercel domain in the `allowed_origins` setting
   - Check that environment variables are properly set in Railway

2. **Database Connection Issues**:
   - Ensure your Railway PostgreSQL plugin is properly attached
   - Verify that the `DATABASE_URL` environment variable is correctly configured

3. **Authentication Failures**:
   - Make sure your `JWT_SECRET_KEY` is set and kept secure
   - Verify that both frontend and backend use the same base URL format (with/without trailing slashes)

### Logging:
- Check Railway's logs for backend issues: `railway logs`
- Check Vercel's logs for frontend issues in the Vercel dashboard
- Use browser dev tools to inspect network requests

## Redeployment

After making changes:
1. Commit and push to your GitHub repository
2. Railway and Vercel will automatically deploy the new version
3. Monitor the deployment status in respective dashboards