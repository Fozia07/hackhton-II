# End-to-End Chatbot Testing Guide
## Complete User Journey Validation

**Date**: 2026-02-15
**Environment**: Minikube with Helm-deployed Todo AI Chatbot
**Namespace**: todo-chatbot
**Frontend URL**: http://localhost:3000
**Test Scope**: Full authentication, chatbot, and MCP integration

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│ Browser (http://localhost:3000)                     │
│ Your Machine                                        │
└───────────────────────┬─────────────────────────────┘
                        │ Port-forward :3000
                        ▼
┌─────────────────────────────────────────────────────┐
│ Kubernetes Cluster (Minikube)                       │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ Frontend Pods (2 ready)                       │   │
│ │ • Serves Next.js UI                          │   │
│ │ • Routes API calls to backend                │   │
│ └──────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼ Service DNS: todo-chatbot-backend
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ Backend Pods (3 ready)                        │   │
│ │ • Handles authentication (Phase II proxy)    │   │
│ │ • Calls Gemini API                           │   │
│ │ • Uses MCP tools                             │   │
│ └──────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼ Service DNS: todo-chatbot-mcp-server:8002
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ MCP Server Pods (2 ready)                     │   │
│ │ • Exposes 5 MCP tools                        │   │
│ │ • Handles database operations                │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Test Scenarios

### Scenario 1: User Sign Up (New Account)

**Objective**: Verify new user registration works end-to-end

**Steps**:
1. ✅ Open http://localhost:3000 in browser
   - Expected: Todo AI Chatbot login page loads
   - Verify: Page shows "Sign Up" button

2. ✅ Click "Sign Up" or navigate to signup
   - Expected: Signup form appears
   - Verify: Fields visible: Email, Username, Password, Confirm Password

3. ✅ Fill signup form:
   ```
   Email: testuser_<timestamp>@example.com
   Username: testuser_<timestamp>
   Password: TestPassword123!
   Confirm: TestPassword123!
   ```
   - Expected: Form accepts input

4. ✅ Click "Sign Up" button
   - Expected: Request sent to `/api/auth/signup`
   - Backend should forward to Phase II auth service
   - Expected response: Account created successfully

5. ✅ Verify redirect to login page
   - Expected: Redirected after 2 seconds
   - New page: Login form with email/password fields

**Pass Criteria**:
- ✅ No error messages
- ✅ Account created on Phase II backend
- ✅ Redirected to login page
- ✅ No "API error 404" messages

**What's Being Tested**:
- Frontend signup component
- Backend auth proxy endpoints
- Phase II authentication service connectivity
- CORS configuration
- GEMINI_API_KEY env var (if used during signup)

---

### Scenario 2: User Sign In (Existing Account)

**Objective**: Verify user authentication works

**Steps**:
1. ✅ On login page, enter credentials:
   ```
   Username: testuser_<timestamp>
   Password: TestPassword123!
   ```

2. ✅ Click "Sign In" button
   - Expected: Request sent to `/api/auth/signin`
   - Backend forwards to Phase II auth service
   - Expected: JWT token returned

3. ✅ Verify token stored in localStorage
   - Open browser DevTools → Application → Local Storage
   - Expected: `jwtToken` key present with token value

4. ✅ Verify redirect to chat page
   - Expected: Redirected to `/chat` URL
   - Expected: Chat interface loads

**Pass Criteria**:
- ✅ No authentication errors
- ✅ JWT token received and stored
- ✅ Chat interface accessible
- ✅ No "Connection error" messages

**What's Being Tested**:
- Phase II authentication service
- JWT token generation
- Token storage in frontend
- Session management
- Backend auth proxy forwarding

---

### Scenario 3: Send Chat Message (AI Response)

**Objective**: Verify end-to-end chatbot functionality with Gemini API

**Steps**:
1. ✅ On chat page, locate message input box
   - Expected: Text input visible at bottom

2. ✅ Type test message:
   ```
   "Hello, what can you do?"
   ```

3. ✅ Press Enter or click Send button
   - Expected: Message appears in chat as "User message"
   - Expected: Loading indicator appears

4. ✅ Wait for AI response (should be < 3 seconds)
   - Expected: AI response appears below user message
   - Expected: Response is from Gemini API (should answer about capabilities)
   - Expected: Tool calls shown (if any)

5. ✅ Verify no error messages
   - Expected: No "API error 404"
   - Expected: No "Sorry, I encountered an API error"
   - Expected: Natural response from AI

**Pass Criteria**:
- ✅ Message sent successfully
- ✅ AI response received within 3 seconds
- ✅ Response is coherent and relevant
- ✅ No error messages in UI
- ✅ No 404 or timeout errors
- ✅ OPENAI_MODEL=gemini-2.5-flash is being used

**What's Being Tested**:
- Frontend message sending
- Backend message processing
- Gemini API integration
- OPENAI_MODEL env var (gemini-2.5-flash)
- AI response generation
- Error handling

---

### Scenario 4: Test MCP Tools (If Available)

**Objective**: Verify MCP tools are available and working

**Steps**:
1. ✅ Send message requesting task creation:
   ```
   "Create a task: Buy groceries"
   ```

2. ✅ Verify AI uses tools:
   - Expected: Response shows "Tool calls:" section
   - Expected: Tool name visible (e.g., "create_task")
   - Expected: Tool result shown

3. ✅ Send message requesting task list:
   ```
   "What tasks do I have?"
   ```

4. ✅ Verify AI retrieves tasks:
   - Expected: AI lists tasks in response
   - Expected: Tool calls shown
   - Expected: Data retrieved from MCP server

**Pass Criteria**:
- ✅ AI recognizes tool requests
- ✅ MCP tools are called successfully
- ✅ Tool results are returned
- ✅ AI incorporates results in response
- ✅ No "unknown tool" errors

**What's Being Tested**:
- MCP server availability
- Tool discovery via `/openmcp.json`
- Backend → MCP server connectivity
- AI tool calling capability
- Database integration

---

### Scenario 5: Error Handling

**Objective**: Verify system handles errors gracefully

**Steps**:
1. ✅ Send invalid request:
   ```
   (Just click send without typing anything)
   ```
   - Expected: Either blocked or handled gracefully

2. ✅ Send very long message (1000+ chars)
   - Expected: Submitted successfully
   - Expected: AI responds within reasonable time

3. ✅ Close browser and reopen
   - Expected: Still logged in (token persisted)
   - Expected: Chat history accessible

4. ✅ Try accessing URL directly without login
   - Open http://localhost:3000/chat without auth
   - Expected: Redirected to login page

**Pass Criteria**:
- ✅ Input validation working
- ✅ Error messages are clear
- ✅ No crashes
- ✅ Session persistence working
- ✅ Auth guards in place

**What's Being Tested**:
- Input validation
- Error handling
- Session management
- Authentication guards
- Frontend routing

---

## Quick Test Checklist

```
PRE-TEST SETUP
[ ] Port-forward running: http://localhost:3000
[ ] Minikube running: minikube status
[ ] All pods ready: kubectl get pods -n todo-chatbot
[ ] Services created: kubectl get svc -n todo-chatbot

SIGN UP TEST
[ ] Open login page
[ ] Click "Sign Up"
[ ] Fill form with unique email/username
[ ] Click "Sign Up" button
[ ] Verify no "Connection error"
[ ] Verify redirect to login
[ ] ✅ PASS

SIGN IN TEST
[ ] Enter credentials
[ ] Click "Sign In"
[ ] Check localStorage for jwtToken
[ ] Verify chat page loads
[ ] ✅ PASS

CHAT MESSAGE TEST
[ ] Type: "Hello, what can you do?"
[ ] Send message
[ ] Verify message appears
[ ] Wait for AI response (< 3 sec)
[ ] Verify response is coherent
[ ] Verify no "API error 404"
[ ] ✅ PASS

MCP TOOLS TEST
[ ] Type: "Create a task: Buy groceries"
[ ] Send message
[ ] Verify tool is called
[ ] Verify task created
[ ] ✅ PASS

OVERALL
[ ] All tests passed
[ ] No errors in browser console
[ ] No errors in pod logs
[ ] ✅ END-TO-END TEST PASSED
```

---

## Debugging Guide

### Issue: "Connection error. Please check that the Phase II backend is running"

**Diagnosis**: Frontend can't reach backend auth endpoints

**Check**:
```bash
# Verify backend is running
kubectl get pods -n todo-chatbot -l component=backend
kubectl logs -n todo-chatbot deployment/todo-chatbot-backend | head -20

# Check auth service URL
kubectl exec -n todo-chatbot pod/todo-chatbot-backend-* -- env | grep AUTH_SERVICE_URL
```

**Solution**:
- Ensure backend pods are Running 1/1 Ready
- Check backend logs for errors
- Verify AUTH_SERVICE_URL environment variable is set

---

### Issue: "Sorry, I encountered an API error: 404"

**Diagnosis**: Gemini API error (this was the issue we fixed!)

**Check**:
```bash
# Verify OPENAI_MODEL is set correctly
kubectl exec -n todo-chatbot pod/todo-chatbot-backend-* -- env | grep OPENAI_MODEL
# Should show: OPENAI_MODEL=gemini-2.5-flash (not gemini-1.5-flash)

# Check backend logs for API errors
kubectl logs -n todo-chatbot deployment/todo-chatbot-backend | grep -i error
```

**Solution**:
- OPENAI_MODEL must be `gemini-2.5-flash` (NOT `gemini-1.5-flash`)
- This was already fixed in our Helm chart!
- Verify with: `kubectl get deployment todo-chatbot-backend -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="OPENAI_MODEL")].value}'`

---

### Issue: Chat message takes > 5 seconds to respond

**Diagnosis**: Slow API or network issue

**Check**:
```bash
# Verify backend can reach Gemini API
kubectl exec -n todo-chatbot pod/todo-chatbot-backend-* -- curl -I https://generativelanguage.googleapis.com/v1beta

# Check pod resources
kubectl top pods -n todo-chatbot

# Check logs for timeouts
kubectl logs -n todo-chatbot deployment/todo-chatbot-backend | grep -i timeout
```

**Solution**:
- Check network connectivity to generativelanguage.googleapis.com
- Verify GEMINI_API_KEY is valid
- Check if pod is resource-constrained

---

### Issue: Tools not being called / "unknown tool"

**Diagnosis**: MCP server issue or tool registration problem

**Check**:
```bash
# Verify MCP server is running
kubectl get pods -n todo-chatbot -l component=mcp-server
kubectl logs -n todo-chatbot deployment/todo-chatbot-mcp-server | head -20

# Check MCP tools are available
kubectl port-forward -n todo-chatbot svc/todo-chatbot-mcp-server 8002:8002 &
curl http://localhost:8002/openmcp.json

# Verify backend can reach MCP server
kubectl exec -n todo-chatbot pod/todo-chatbot-backend-* -- curl http://todo-chatbot-mcp-server:8002/health
```

**Solution**:
- Ensure MCP server pods are Running 1/1 Ready
- Verify MCP_SERVER_URL in backend is `http://todo-chatbot-mcp-server:8002`
- Check MCP server logs for errors

---

## Expected Results Summary

### ✅ What Should Work

| Component | Expected Behavior | Status |
|-----------|-------------------|--------|
| **Frontend** | Loads at http://localhost:3000 | ✅ Ready |
| **Login/Signup** | Works with Phase II auth | ✅ Ready |
| **JWT Token** | Stored in localStorage | ✅ Ready |
| **Chat Interface** | Loads after login | ✅ Ready |
| **Message Sending** | Messages appear in chat | ✅ Ready |
| **Gemini API** | Responds with gemini-2.5-flash | ✅ Fixed |
| **MCP Tools** | Available in /openmcp.json | ✅ Deployed |
| **Tool Calling** | AI calls tools when appropriate | ✅ Ready |
| **Error Handling** | Clear error messages | ✅ Ready |
| **Session Mgmt** | Login persists across refresh | ✅ Ready |

### ❌ What Should NOT Happen

| Issue | Status |
|-------|--------|
| 404 errors from Gemini API | ✅ FIXED (was gemini-1.5-flash, now 2.5-flash) |
| "Connection error" on signup | ✅ FIXED (backend auth proxy working) |
| MCP server unreachable | ✅ FIXED (included in Helm chart) |
| Pods not starting | ✅ FIXED (working via Helm) |
| Service discovery failing | ✅ FIXED (DNS working) |

---

## Testing Command Cheat Sheet

```bash
# Start fresh port-forward
kubectl port-forward -n todo-chatbot svc/todo-chatbot-frontend 3000:80

# Check all pods
kubectl get pods -n todo-chatbot -o wide

# View backend logs
kubectl logs -n todo-chatbot deployment/todo-chatbot-backend -f

# Check environment variables
kubectl exec -n todo-chatbot pod/todo-chatbot-backend-* -- env | grep -E "OPENAI|AUTH|MCP"

# Test backend health
kubectl port-forward -n todo-chatbot svc/todo-chatbot-backend 8000:80 &
curl http://localhost:8000/health

# Test MCP server
kubectl port-forward -n todo-chatbot svc/todo-chatbot-mcp-server 8002:8002 &
curl http://localhost:8002/docs

# Check Helm status
helm status todo-chatbot -n todo-chatbot

# View pod details
kubectl describe pod -n todo-chatbot <pod-name>

# Stream logs from all backend pods
kubectl logs -n todo-chatbot deployment/todo-chatbot-backend -f --all-containers
```

---

## Post-Test Validation

After running through all scenarios, verify:

**In Browser DevTools Console**:
- [ ] No JavaScript errors
- [ ] No network errors (404, 500)
- [ ] API calls returning 2xx status codes
- [ ] jwtToken present in localStorage

**In Kubernetes**:
- [ ] All pods still Running 1/1 Ready
- [ ] No pods in CrashLoopBackOff
- [ ] No recent restarts (Age shows steady)
- [ ] Services have active endpoints

**In Pod Logs**:
- [ ] No error stacktraces
- [ ] No timeout errors
- [ ] API calls logged successfully
- [ ] Auth flows completed

---

## Success Criteria

**Test is SUCCESSFUL if**:
✅ User can sign up with new account
✅ User can sign in and get JWT token
✅ Chat interface loads after authentication
✅ User can send messages
✅ AI responds with Gemini API (gemini-2.5-flash)
✅ Response arrives within 3 seconds
✅ No "API error 404" messages
✅ MCP tools are available (if tested)
✅ All pods remain Running 1/1 Ready
✅ No errors in logs or console

---

## Test Report Template

```markdown
# End-to-End Test Report

**Date**: [Date]
**Tester**: [Your name]
**Environment**: Minikube with Helm deployment

## Test Results

### Sign Up
- [ ] ✅ PASS - Account created
- [ ] ❌ FAIL - [Issue description]
- Notes: [Any observations]

### Sign In
- [ ] ✅ PASS - Token received
- [ ] ❌ FAIL - [Issue description]
- Notes: [Any observations]

### Chat Message
- [ ] ✅ PASS - AI responded
- [ ] ❌ FAIL - [Issue description]
- Notes: Response time: [seconds]

### MCP Tools
- [ ] ✅ PASS - Tools called
- [ ] ❌ FAIL - [Issue description]
- Notes: [Any observations]

## Overall Result
- [ ] ✅ **PASS** - All tests successful
- [ ] ❌ **FAIL** - [Blocking issue]

## Issues Found
[List any issues and severity]

## Logs Attached
- backend-logs.txt
- frontend-console.log
```

---

## Next Steps

After successful E2E testing:

1. **Commit Test Results**
   - Record any issues or learnings
   - Update documentation

2. **Create PR**
   - All implementation complete
   - All tests passing
   - Ready for code review

3. **Plan Production Deployment**
   - Decide on cloud provider (EKS, GKE, AKS)
   - Configure production values
   - Set up monitoring and logging

4. **Optional Enhancements**
   - Add more MCP tools
   - Implement additional features
   - Performance optimization

---

## Summary

The Todo AI Chatbot is now ready for end-to-end testing. All infrastructure components are deployed via Helm and running:

- **Frontend**: Next.js UI with authentication
- **Backend**: FastAPI with Gemini API integration
- **MCP Server**: Model Context Protocol with database tools
- **Authentication**: Phase II backend proxy
- **API**: Gemini 2.5 Flash model

**All critical issues are fixed** and the system should work end-to-end.

**Start testing at**: http://localhost:3000

---

**Document Version**: 1.0
**Last Updated**: 2026-02-15
**Status**: Ready for E2E Testing
