# FastAPI WebSockets & Real-Time Communication

## Expertise
Expert skill for implementing WebSocket connections and real-time communication in FastAPI applications. Specializes in WebSocket endpoints, connection management, broadcasting, room patterns, authentication, and production-ready real-time features.

## Purpose
This skill handles real-time communication, enabling you to:
- Establish WebSocket connections
- Send and receive messages in real-time
- Broadcast messages to multiple clients
- Implement chat rooms and channels
- Authenticate WebSocket connections
- Handle connection lifecycle (connect, disconnect, reconnect)
- Implement presence tracking (online/offline status)
- Build real-time dashboards and notifications
- Handle connection errors and recovery

## When to Use
Use this skill when you need to:
- Build chat applications
- Implement real-time notifications
- Create live dashboards with streaming data
- Build collaborative editing features
- Implement live updates (stock prices, sports scores)
- Create multiplayer game features
- Build real-time monitoring systems
- Implement presence indicators (typing, online status)

## Core Concepts

### 1. Basic WebSocket Connection

**Simple WebSocket Endpoint**:
```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Basic WebSocket endpoint.
    Accepts connection and echoes messages back.
    """
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            # Send message back to client
            await websocket.send_text(f"Message received: {data}")

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
```

**WebSocket with JSON Messages**:
```python
import json

@app.websocket("/ws/json")
async def websocket_json(websocket: WebSocket):
    """WebSocket endpoint with JSON messages."""
    await websocket.accept()

    try:
        while True:
            # Receive JSON message
            data = await websocket.receive_json()

            # Process message
            response = {
                "type": "echo",
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Send JSON response
            await websocket.send_json(response)

    except Exception as e:
        print(f"WebSocket error: {e}")
```

**Client-Side HTML Example**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h1>WebSocket Test</h1>
    <input id="messageInput" type="text" placeholder="Enter message">
    <button onclick="sendMessage()">Send</button>
    <div id="messages"></div>

    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");

        ws.onopen = function(event) {
            console.log("Connected to WebSocket");
            addMessage("Connected to server");
        };

        ws.onmessage = function(event) {
            console.log("Message from server:", event.data);
            addMessage("Server: " + event.data);
        };

        ws.onerror = function(error) {
            console.error("WebSocket error:", error);
            addMessage("Error: " + error);
        };

        ws.onclose = function(event) {
            console.log("WebSocket closed");
            addMessage("Disconnected from server");
        };

        function sendMessage() {
            const input = document.getElementById("messageInput");
            const message = input.value;
            ws.send(message);
            addMessage("You: " + message);
            input.value = "";
        }

        function addMessage(message) {
            const messagesDiv = document.getElementById("messages");
            messagesDiv.innerHTML += "<p>" + message + "</p>";
        }
    </script>
</body>
</html>
```

### 2. Connection Manager

**WebSocket Connection Manager**:
```python
from typing import List, Dict
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages WebSocket connections.
    Handles multiple clients and broadcasting.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and store new connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove connection."""
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific client."""
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """Send message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, message: dict):
        """Send JSON message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_json(message)

# Create global connection manager
manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_with_manager(websocket: WebSocket, client_id: int):
    """WebSocket endpoint using connection manager."""
    await manager.connect(websocket)

    try:
        # Notify all clients about new connection
        await manager.broadcast(f"Client #{client_id} joined the chat")

        while True:
            data = await websocket.receive_text()

            # Send personal message
            await manager.send_personal_message(f"You wrote: {data}", websocket)

            # Broadcast to all
            await manager.broadcast(f"Client #{client_id} says: {data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
```

### 3. Room-Based WebSockets (Chat Rooms)

**Room Manager**:
```python
from typing import Dict, Set

class RoomManager:
    """
    Manages WebSocket connections organized by rooms.
    Supports multiple chat rooms or channels.
    """

    def __init__(self):
        # room_id -> set of WebSocket connections
        self.rooms: Dict[str, Set[WebSocket]] = {}
        # websocket -> room_id mapping
        self.connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        """Connect client to specific room."""
        await websocket.accept()

        # Create room if doesn't exist
        if room_id not in self.rooms:
            self.rooms[room_id] = set()

        # Add connection to room
        self.rooms[room_id].add(websocket)
        self.connections[websocket] = room_id

    def disconnect(self, websocket: WebSocket):
        """Disconnect client from room."""
        if websocket in self.connections:
            room_id = self.connections[websocket]
            self.rooms[room_id].discard(websocket)
            del self.connections[websocket]

            # Clean up empty rooms
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def send_to_room(self, room_id: str, message: dict):
        """Send message to all clients in specific room."""
        if room_id in self.rooms:
            for connection in self.rooms[room_id]:
                await connection.send_json(message)

    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send message to specific client."""
        await websocket.send_json(message)

    def get_room_size(self, room_id: str) -> int:
        """Get number of clients in room."""
        return len(self.rooms.get(room_id, set()))

# Create global room manager
room_manager = RoomManager()

@app.websocket("/ws/room/{room_id}")
async def websocket_room(websocket: WebSocket, room_id: str):
    """WebSocket endpoint for chat rooms."""
    await room_manager.connect(websocket, room_id)

    try:
        # Notify room about new user
        await room_manager.send_to_room(
            room_id,
            {
                "type": "user_joined",
                "room_id": room_id,
                "users_count": room_manager.get_room_size(room_id)
            }
        )

        while True:
            data = await websocket.receive_json()

            # Broadcast message to room
            await room_manager.send_to_room(
                room_id,
                {
                    "type": "message",
                    "room_id": room_id,
                    "message": data.get("message"),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        room_manager.disconnect(websocket)

        # Notify room about user leaving
        await room_manager.send_to_room(
            room_id,
            {
                "type": "user_left",
                "room_id": room_id,
                "users_count": room_manager.get_room_size(room_id)
            }
        )
```

### 4. WebSocket Authentication

**Token-Based Authentication**:
```python
from fastapi import WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from core.config import get_settings

settings = get_settings()

async def get_user_from_token(token: str) -> dict:
    """
    Validate JWT token and return user info.

    Args:
        token: JWT token

    Returns:
        User info dict

    Raises:
        WebSocketDisconnect: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        raise WebSocketDisconnect(code=1008, reason="Invalid token")

@app.websocket("/ws/authenticated")
async def websocket_authenticated(
    websocket: WebSocket,
    token: str = Query(...)
):
    """
    Authenticated WebSocket endpoint.
    Token passed as query parameter: ws://localhost:8000/ws/authenticated?token=xxx
    """
    # Validate token before accepting connection
    try:
        user = await get_user_from_token(token)
    except WebSocketDisconnect:
        await websocket.close(code=1008, reason="Invalid token")
        return

    await websocket.accept()

    try:
        # Send welcome message with user info
        await websocket.send_json({
            "type": "welcome",
            "user": user
        })

        while True:
            data = await websocket.receive_json()

            # Process authenticated message
            response = {
                "type": "message",
                "user_id": user["sub"],
                "data": data
            }
            await websocket.send_json(response)

    except WebSocketDisconnect:
        print(f"User {user['sub']} disconnected")
```

**Cookie-Based Authentication**:
```python
from fastapi import Cookie

@app.websocket("/ws/cookie-auth")
async def websocket_cookie_auth(
    websocket: WebSocket,
    session_token: str = Cookie(None)
):
    """WebSocket with cookie-based authentication."""
    if not session_token:
        await websocket.close(code=1008, reason="No session token")
        return

    # Validate session token
    user = await validate_session(session_token)
    if not user:
        await websocket.close(code=1008, reason="Invalid session")
        return

    await websocket.accept()

    # Continue with authenticated connection
    # ...
```

### 5. Advanced Connection Manager with User Tracking

**Enhanced Connection Manager**:
```python
from typing import Dict, Set
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Connection:
    """WebSocket connection with metadata."""
    websocket: WebSocket
    user_id: int
    username: str
    connected_at: datetime

class AdvancedConnectionManager:
    """
    Advanced connection manager with user tracking.
    Supports multiple connections per user and presence tracking.
    """

    def __init__(self):
        # user_id -> set of Connection objects
        self.user_connections: Dict[int, Set[Connection]] = {}
        # websocket -> Connection object
        self.connections: Dict[WebSocket, Connection] = {}

    async def connect(
        self,
        websocket: WebSocket,
        user_id: int,
        username: str
    ):
        """Connect user with metadata."""
        await websocket.accept()

        connection = Connection(
            websocket=websocket,
            user_id=user_id,
            username=username,
            connected_at=datetime.utcnow()
        )

        # Add to user connections
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection)

        # Add to connections map
        self.connections[websocket] = connection

    def disconnect(self, websocket: WebSocket):
        """Disconnect user."""
        if websocket in self.connections:
            connection = self.connections[websocket]
            user_id = connection.user_id

            # Remove from user connections
            self.user_connections[user_id].discard(connection)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

            # Remove from connections map
            del self.connections[websocket]

    async def send_to_user(self, user_id: int, message: dict):
        """Send message to all connections of specific user."""
        if user_id in self.user_connections:
            for connection in self.user_connections[user_id]:
                await connection.websocket.send_json(message)

    async def broadcast(self, message: dict, exclude_user: int = None):
        """Broadcast message to all users except specified user."""
        for user_id, connections in self.user_connections.items():
            if exclude_user and user_id == exclude_user:
                continue

            for connection in connections:
                await connection.websocket.send_json(message)

    def is_user_online(self, user_id: int) -> bool:
        """Check if user has any active connections."""
        return user_id in self.user_connections

    def get_online_users(self) -> List[dict]:
        """Get list of online users."""
        return [
            {
                "user_id": user_id,
                "username": next(iter(connections)).username,
                "connections": len(connections)
            }
            for user_id, connections in self.user_connections.items()
        ]

# Create global advanced manager
advanced_manager = AdvancedConnectionManager()

@app.websocket("/ws/advanced")
async def websocket_advanced(
    websocket: WebSocket,
    token: str = Query(...)
):
    """Advanced WebSocket with user tracking."""
    # Authenticate
    user = await get_user_from_token(token)
    user_id = int(user["sub"])
    username = user.get("username", "Anonymous")

    # Connect
    await advanced_manager.connect(websocket, user_id, username)

    try:
        # Notify others about new user
        await advanced_manager.broadcast(
            {
                "type": "user_online",
                "user_id": user_id,
                "username": username
            },
            exclude_user=user_id
        )

        # Send online users list to new user
        await advanced_manager.send_to_user(
            user_id,
            {
                "type": "online_users",
                "users": advanced_manager.get_online_users()
            }
        )

        while True:
            data = await websocket.receive_json()

            # Handle different message types
            if data["type"] == "message":
                await advanced_manager.broadcast({
                    "type": "message",
                    "user_id": user_id,
                    "username": username,
                    "message": data["message"],
                    "timestamp": datetime.utcnow().isoformat()
                })

            elif data["type"] == "typing":
                await advanced_manager.broadcast(
                    {
                        "type": "typing",
                        "user_id": user_id,
                        "username": username
                    },
                    exclude_user=user_id
                )

    except WebSocketDisconnect:
        pass
    finally:
        advanced_manager.disconnect(websocket)

        # Notify others if user is completely offline
        if not advanced_manager.is_user_online(user_id):
            await advanced_manager.broadcast({
                "type": "user_offline",
                "user_id": user_id,
                "username": username
            })
```

### 6. Error Handling and Reconnection

**Graceful Error Handling**:
```python
from fastapi import WebSocketDisconnect

@app.websocket("/ws/robust")
async def websocket_robust(websocket: WebSocket):
    """WebSocket with robust error handling."""
    await websocket.accept()

    try:
        while True:
            try:
                # Receive message with timeout
                data = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=60.0  # 60 second timeout
                )

                # Process message
                await websocket.send_json({
                    "type": "ack",
                    "data": data
                })

            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_json({"type": "ping"})

            except json.JSONDecodeError:
                # Handle invalid JSON
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })

    except WebSocketDisconnect:
        print("Client disconnected normally")

    except Exception as e:
        print(f"Unexpected error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass
```

**Client-Side Reconnection Logic**:
```javascript
class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log("Connected");
            this.reconnectAttempts = 0;
            this.reconnectDelay = 1000;
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        this.ws.onclose = () => {
            console.log("Disconnected");
            this.reconnect();
        };
    }

    reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error("Max reconnection attempts reached");
            return;
        }

        this.reconnectAttempts++;
        console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);

        setTimeout(() => {
            this.connect();
        }, this.reconnectDelay);

        // Exponential backoff
        this.reconnectDelay *= 2;
    }

    send(data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.error("WebSocket not connected");
        }
    }

    handleMessage(data) {
        // Override this method to handle messages
        console.log("Message received:", data);
    }
}
```

### 7. Real-Time Notifications

**Notification System**:
```python
@app.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(
    websocket: WebSocket,
    user_id: int,
    token: str = Query(...)
):
    """WebSocket endpoint for real-time notifications."""
    # Authenticate
    user = await get_user_from_token(token)
    if int(user["sub"]) != user_id:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    await websocket.accept()

    try:
        # Send pending notifications
        pending = await get_pending_notifications(user_id)
        for notification in pending:
            await websocket.send_json({
                "type": "notification",
                "data": notification
            })

        # Keep connection alive and listen for new notifications
        while True:
            # Wait for new notifications (from background task or event)
            notification = await wait_for_notification(user_id)
            await websocket.send_json({
                "type": "notification",
                "data": notification
            })

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected from notifications")
```

## Best Practices

### 1. Connection Management
- Use connection managers for multiple clients
- Track connection metadata (user, timestamp)
- Implement graceful disconnection
- Clean up resources on disconnect
- Handle multiple connections per user

### 2. Message Format
- Use consistent message structure (type, data, timestamp)
- Validate incoming messages
- Use JSON for structured data
- Include message IDs for tracking
- Implement message acknowledgments

### 3. Error Handling
- Handle WebSocketDisconnect gracefully
- Implement timeout for idle connections
- Send error messages to clients
- Log all errors with context
- Implement reconnection logic on client

### 4. Security
- Always authenticate WebSocket connections
- Validate tokens before accepting
- Implement rate limiting
- Sanitize user input
- Use secure WebSocket (wss://) in production

### 5. Performance
- Avoid blocking operations in WebSocket handlers
- Use async operations throughout
- Implement message queuing for high volume
- Consider Redis for distributed WebSocket support
- Monitor connection counts and memory usage

### 6. Scalability
- Use Redis Pub/Sub for multi-server deployments
- Implement sticky sessions for load balancing
- Consider WebSocket-specific load balancers
- Monitor and limit concurrent connections
- Implement connection pooling

## Summary

This skill provides comprehensive guidance for implementing WebSockets in FastAPI applications with:
- Basic WebSocket connections and message handling
- Connection managers for multiple clients
- Room-based WebSocket patterns for chat
- Authentication strategies (token, cookie)
- Advanced connection management with user tracking
- Error handling and reconnection strategies
- Real-time notification systems
- Best practices for security, performance, and scalability

Use this skill to build real-time features in your FastAPI applications with proper connection management, authentication, and error handling for production environments.
