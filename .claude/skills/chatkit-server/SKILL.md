---
name: chatkit-server
description: |
  Builds conversational AI backends using OpenAI ChatKit Server framework, from hello world to production systems.
  This skill should be used when users want to create chat applications, implement AI assistants with streaming responses,
  build conversational interfaces with tools and widgets, integrate OpenAI Agents SDK, or set up production-ready chat backends.
  Handles server setup, agent integration, data persistence, tool execution, and deployment patterns.
---

# ChatKit Server

Build conversational AI backends from hello world to production systems using OpenAI ChatKit Server.

## What This Skill Does

- Creates ChatKit Server implementations with FastAPI
- Integrates OpenAI Agents SDK for AI-powered conversations
- Implements streaming responses with Server-Sent Events (SSE)
- Sets up data stores (Memory, PostgreSQL, custom)
- Configures tools, widgets, and attachments
- Provides production deployment patterns

## What This Skill Does NOT Do

- Build frontend chat UIs (use ChatKit React components separately)
- Handle authentication/authorization (implement separately)
- Manage infrastructure provisioning
- Deploy to specific cloud providers (provides patterns only)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI apps, database setup, project structure |
| **Conversation** | User's requirements: use case, features, deployment target |
| **Skill References** | ChatKit patterns from `references/` (architecture, examples, best practices) |
| **User Guidelines** | Team conventions, security requirements, tech stack constraints |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Implementation Levels

ChatKit Server supports progressive complexity:

| Level | Capability | When to Use |
|-------|-----------|-------------|
| **Hello World** | Basic echo server | Learning, prototyping |
| **Agent-Powered** | OpenAI Agents SDK integration | AI assistants, conversational AI |
| **Tools & Widgets** | Custom tools, rich UI components | Interactive experiences |
| **Production** | Persistence, error handling, monitoring | Real applications |

Start at the appropriate level for user's needs.

---

## Core Workflow

### 1. Clarify Requirements

Ask user about THEIR specific needs:

| Question | Purpose |
|----------|---------|
| **Use case** | What type of conversational experience? (support bot, assistant, etc.) |
| **Features** | Streaming? Tools? Widgets? File attachments? |
| **Data store** | In-memory (dev) or persistent (PostgreSQL, Redis)? |
| **Deployment** | Local dev, cloud platform, existing infrastructure? |
| **Existing code** | Integrating with existing FastAPI app or new project? |

### 2. Choose Architecture Pattern

Based on requirements, select pattern from `references/architecture.md`:

- **Minimal**: Echo server for learning
- **Agent-Based**: OpenAI Agents SDK integration
- **Tool-Enabled**: Custom function tools
- **Widget-Rich**: Streaming UI components
- **Production**: Full persistence and error handling

### 3. Implement Server Class

Create custom `ChatKitServer` subclass:

```python
class MyChatKitServer(ChatKitServer):
    def __init__(self, data_store: Store, attachment_store: AttachmentStore | None = None):
        super().__init__(data_store, attachment_store)

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        # Implementation based on chosen pattern
        pass
```

### 4. Set Up FastAPI Endpoint

Configure `/chatkit` endpoint:

```python
@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    else:
        return Response(content=result.json, media_type="application/json")
```

### 5. Configure Data Store

Set up appropriate store based on requirements:

- **Development**: `MemoryStore()` (in-memory, ephemeral)
- **Production**: `PostgresStore()` (persistent, scalable)
- **Custom**: Implement `Store` interface

### 6. Add Features Progressively

Based on user needs:

- **Agents SDK**: Use `stream_agent_response()` helper
- **Tools**: Define with `@function_tool` decorator
- **Widgets**: Yield widget events in respond()
- **Attachments**: Configure `AttachmentStore`

### 7. Test and Deploy

- Test locally with `uvicorn --reload`
- Add error handling and logging
- Configure environment variables
- Deploy following production patterns

---

## Quick Start Examples

### Hello World (Echo Server)

Simplest possible ChatKit server:

```python
from chatkit.server import ChatKitServer, ThreadMetadata, UserMessageItem
from chatkit.types import ThreadStreamEvent, AssistantMessageItem

class EchoServer(ChatKitServer):
    async def respond(self, thread, input, context):
        if input:
            yield AssistantMessageItem(content=f"Echo: {input.content}")
```

### Agent-Powered Server

Integrate OpenAI Agents SDK:

```python
from chatkit.server import ChatKitServer, stream_agent_response
from agents import Agent, Runner

class AgentServer(ChatKitServer):
    assistant = Agent(
        model="gpt-4o",
        name="Assistant",
        instructions="You are a helpful assistant"
    )

    async def respond(self, thread, input, context):
        result = Runner.run_streamed(self.assistant, [input])
        async for event in stream_agent_response(context, result):
            yield event
```

See `references/quickstart.md` for complete examples.

---

## Key Concepts

### ChatKitServer Base Class

Core abstraction for building chat backends:

- **`respond()` method**: Implement to define conversation logic
- **Streaming**: Yield `ThreadStreamEvent` objects for real-time updates
- **Context**: Access thread metadata, user input, request context
- **Store integration**: Automatic persistence of conversations

### Thread Management

ChatKit manages conversation threads automatically:

- **ThreadMetadata**: Thread ID, creation time, metadata
- **Message history**: Stored in configured data store
- **Context preservation**: Threads maintain conversation state

### Event Streaming

Server-Sent Events (SSE) for real-time updates:

- **StreamingResult**: Returned for SSE responses
- **ThreadStreamEvent**: Base type for all events
- **Event types**: Messages, tool calls, widgets, status updates

### Data Stores

Pluggable persistence layer:

- **MemoryStore**: In-memory (development)
- **PostgresStore**: PostgreSQL (production)
- **Custom stores**: Implement `Store` interface

---

## Common Patterns

### Pattern: Agent with Tools

```python
@function_tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

class ToolServer(ChatKitServer):
    agent = Agent(
        model="gpt-4o",
        tools=[get_weather],
        instructions="Help users with weather information"
    )
```

### Pattern: Streaming Widgets

```python
async def respond(self, thread, input, context):
    # Stream a widget
    yield WidgetEvent(
        widget_type="chart",
        data={"values": [1, 2, 3]}
    )

    # Stream assistant message
    yield AssistantMessageItem(content="Here's your chart!")
```

### Pattern: Error Handling

```python
async def respond(self, thread, input, context):
    try:
        # Process request
        result = await process_input(input)
        yield result
    except Exception as e:
        logger.error(f"Error processing: {e}")
        yield AssistantMessageItem(
            content="I encountered an error. Please try again."
        )
```

See `references/architecture.md` for complete patterns.

---

## Dependencies

### Required Packages

```bash
pip install chatkit-python openai-agents-sdk fastapi uvicorn
```

### Optional Packages

```bash
# PostgreSQL support
pip install psycopg2-binary

# Development tools
pip install uv  # Fast package manager
```

### Environment Variables

```bash
OPENAI_API_KEY=sk-proj-...  # Required for OpenAI models
DATABASE_URL=postgresql://...  # For PostgresStore
```

---

## Production Checklist

Before deploying to production:

- [ ] Replace `MemoryStore` with persistent store (PostgreSQL, Redis)
- [ ] Add comprehensive error handling and logging
- [ ] Configure CORS for frontend domain
- [ ] Set up environment variable management
- [ ] Implement rate limiting
- [ ] Add monitoring and observability
- [ ] Configure secure attachment storage
- [ ] Test streaming behavior under load
- [ ] Document API endpoints
- [ ] Set up CI/CD pipeline

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Streaming not working** | Ensure `StreamingResponse` with `media_type="text/event-stream"` |
| **Agent not responding** | Check `OPENAI_API_KEY` is set correctly |
| **Store errors** | Verify database connection and schema |
| **CORS errors** | Configure FastAPI CORS middleware |
| **Import errors** | Install all required packages: `chatkit-python`, `openai-agents-sdk` |

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Reference Files

| File | Content |
|------|---------|
| `references/architecture.md` | Server patterns, design decisions, scaling strategies |
| `references/quickstart.md` | Complete working examples from hello world to production |
| `references/agents-integration.md` | OpenAI Agents SDK integration patterns and helpers |
| `references/tools-widgets.md` | Custom tools, widgets, and advanced features |

---

## Example: Complete Production Server

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from chatkit.server import ChatKitServer, StreamingResult, stream_agent_response
from chatkit.stores import PostgresStore
from agents import Agent, Runner
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="ChatKit Production Server")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize stores
data_store = PostgresStore(database_url=os.getenv("DATABASE_URL"))

# Define ChatKit server
class ProductionChatServer(ChatKitServer):
    def __init__(self, data_store):
        super().__init__(data_store)

    assistant = Agent(
        model="gpt-4o",
        name="Assistant",
        instructions="You are a helpful production assistant"
    )

    async def respond(self, thread, input, context):
        try:
            result = Runner.run_streamed(self.assistant, [input])
            async for event in stream_agent_response(context, result):
                yield event
        except Exception as e:
            logger.error(f"Error in respond: {e}", exc_info=True)
            raise

# Initialize server
server = ProductionChatServer(data_store)

# ChatKit endpoint
@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    try:
        result = await server.process(await request.body(), {"request": request})
        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        else:
            return Response(content=result.json, media_type="application/json")
    except Exception as e:
        logger.error(f"Error in endpoint: {e}", exc_info=True)
        return Response(content={"error": str(e)}, status_code=500)

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run with:
```bash
export OPENAI_API_KEY=sk-proj-...
export DATABASE_URL=postgresql://user:pass@localhost/chatkit
uvicorn main:app --reload
```

---

## Next Steps

After implementing basic server:

1. **Add Tools**: Define custom functions for your domain
2. **Implement Widgets**: Create rich UI components
3. **Configure Persistence**: Set up production database
4. **Add Monitoring**: Integrate logging and metrics
5. **Deploy**: Follow production deployment patterns
6. **Iterate**: Add features based on user feedback

See reference files for detailed guidance on each step.
