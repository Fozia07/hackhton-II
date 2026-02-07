# Quickstart Guide: Authentication Identity Fix

## Overview
This guide explains how to implement the fix for the 403 authentication error in the Todo AI Chatbot application. The issue occurs when the username in API path parameters doesn't match the username in the JWT token.

## Prerequisites
- Node.js and npm installed
- Python environment with FastAPI
- Phase II backend running on http://127.0.0.1:8001
- Phase III backend running on http://127.0.0.1:8000

## Setup
1. Clone the repository and navigate to the frontend directory
2. Install dependencies: `npm install`
3. Ensure your .env.local has the correct backend URL

## Implementation Steps

### 1. Update Login Handler
Modify the login success handler to extract and store the canonical username:

- In `src/app/login/page.tsx`, update the response parsing to get the username from the API response
- Store the canonical username instead of the user's input

### 2. Verify API Client
Ensure the API client uses the stored username consistently:

- In `src/lib/api.ts`, verify that the username parameter matches the stored canonical username
- Make sure the path parameter format is consistent

### 3. Test Authentication Flow
1. Log in with email address (if that's how you normally log in)
2. Verify that the correct username is stored in localStorage
3. Try sending a message in the chat
4. Confirm that you get a 200 response instead of 403

## Troubleshooting
- If 403 errors persist, check localStorage to ensure correct username is stored
- Verify that the JWT token contains the expected username claim
- Check browser network tab to confirm API calls use correct path parameter