---
id: 012
title: Create FastAPI WebSockets Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["fastapi", "websockets", "skill-creation", "real-time", "chat", "notifications"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-websockets.md
tests:
  - none (documentation work)
---

## Prompt

Continue (implicit: continue building FastAPI skills ecosystem)

## Response snapshot

Created comprehensive FastAPI WebSockets & Real-Time Communication skill documentation (25K) at `.claude/skills/fastapi-websockets.md`.

The skill covers:

**1. Basic WebSocket Connection**
- Simple WebSocket endpoint with echo pattern
- WebSocket with JSON messages
- Client-side HTML example with JavaScript WebSocket API

**2. Connection Manager**
- WebSocket connection manager for multiple clients
- Connection tracking and lifecycle management
- Personal messages and broadcasting
- Client join/leave notifications

**3. Room-Based WebSockets (Chat Rooms)**
- RoomManager for organizing connections by rooms/channels
- Room creation and cleanup
- Room-specific broadcasting
- User count tracking per room

**4. WebSocket Authentication**
- Token-based authentication with JWT (query parameter)
- Cookie-based authentication
- Token validation before accepting connections
- Authenticated message handling

**5. Advanced Connection Manager with User Tracking**
- Enhanced connection manager with metadata
- Multiple connections per user support
- User presence tracking (online/offline)
- Typing indicators
- Online users list
- Broadcast with exclusions

**6. Error Handling and Reconnection**
- Graceful error handling with timeouts
- WebSocketDisconnect handling
- JSON parsing error handling
- Client-side reconnection logic with exponential backoff
- Connection state management

**7. Real-Time Notifications**
- Notification system over WebSocket
- Pending notifications delivery
- Real-time notification streaming

**Best Practices**:
- Connection management (managers, metadata, graceful disconnect, cleanup, multiple connections)
- Message format (consistent structure, validation, JSON, message IDs, acknowledgments)
- Error handling (graceful disconnect, timeouts, error messages, logging, reconnection)
- Security (authentication, token validation, rate limiting, input sanitization, wss://)
- Performance (async operations, message queuing, Redis for distributed, monitoring)
- Scalability (Redis Pub/Sub, sticky sessions, load balancers, connection limits, pooling)

The skill completes the real-time communication layer for FastAPI applications, enabling chat, notifications, live updates, and collaborative features.

## Outcome

- ✅ Impact: Created production-ready FastAPI WebSockets skill with comprehensive patterns for real-time communication, connection management, authentication, room-based chat, and error handling
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/fastapi-websockets.md (25K)
- 🔁 Next prompts: User may request additional FastAPI skills (caching, rate limiting, middleware, monitoring, GraphQL) or begin implementing a FastAPI application with full real-time capabilities
- 🧠 Reflection: This skill adds critical real-time communication capabilities to the FastAPI ecosystem. Combined with existing skills (routing, validation, security, configuration, testing, database, migrations, background tasks, file handling), developers can now build APIs with WebSocket support for chat, notifications, live dashboards, and collaborative features with proper authentication, error handling, and scalability patterns for production environments.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
