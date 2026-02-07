# ChatKit Server Architecture

Comprehensive guide to ChatKit Server patterns, design decisions, and scaling strategies.

---

## Server Patterns

### Pattern 1: Minimal Echo Server

**Use case**: Learning, prototyping, testing infrastructure

```python
from chatkit.server import ChatKitServer, ThreadMetadata, UserMessageItem
from chatkit.types import ThreadStreamEvent, AssistantMessageItem
from chatkit.stores import MemoryStore

class EchoServer(ChatKitServer):
    def __init__(self):
        super().__init__(MemoryStore())

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        if input:
            yield AssistantMessageItem(content=f"Echo: {input.content}")
```

**Characteristics**:
- No AI model required
- In-memory storage (ephemeral)
- Minimal dependencies
- Fast iteration

---

### Pattern 2: Agent-Based Server

**Use case**: AI-powered conversations, assistants, chatbots

```python
from chatkit.server import ChatKitServer, stream_agent_response
from chatkit.stores import MemoryStore
from agents import Agent, Runner
from chatkit.helpers import simple_to_agent_input

class AgentServer(ChatKitServer):
    def __init__(self, data_store):
        super().__init__(data_store)

    assistant_agent = Agent(
        model="gpt-4o",
        name="Assistant",
        instructions="You are a helpful assistant"
    )

    async def respond(self, thread, input, context):
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        result = Runner.run_streamed(
            self.assistant_agent,
            await simple_to_agent_input(input) if input else [],
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, result):
            yield event
```

**Characteristics**:
- OpenAI Agents SDK integration
- Streaming responses
- Automatic conversation history
- Model-powered intelligence

**Key Helper**: `stream_agent_response()` converts Agents SDK runs into ChatKit events

---

### Pattern 3: Tool-Enabled Server

**Use case**: Function calling, external integrations, data retrieval

```python
from agents import Agent, function_tool

@function_tool
def search_database(query: str) -> str:
    """Search the knowledge database."""
    # Implementation
    return f"Results for: {query}"

@function_tool
def get_user_info(user_id: str) -> dict:
    """Get user information."""
    return {"id": user_id, "name": "John Doe"}

class ToolServer(ChatKitServer):
    assistant = Agent(
        model="gpt-4o",
        name="Assistant",
        instructions="You help users find information",
        tools=[search_database, get_user_info]
    )

    async def respond(self, thread, input, context):
        result = Runner.run_streamed(self.assistant, [input])
        async for event in stream_agent_response(context, result):
            yield event
```

**Characteristics**:
- Custom function tools
- Automatic tool calling by AI
- Structured outputs
- External system integration

---

### Pattern 4: Widget-Rich Server

**Use case**: Rich UI components, data visualizations, interactive elements

```python
from chatkit.types import WidgetEvent

class WidgetServer(ChatKitServer):
    async def respond(self, thread, input, context):
        # Analyze request
        if "chart" in input.content.lower():
            # Stream a chart widget
            yield WidgetEvent(
                widget_type="chart",
                data={
                    "type": "bar",
                    "values": [10, 20, 30, 40],
                    "labels": ["Q1", "Q2", "Q3", "Q4"]
                }
            )

        # Stream explanation
        yield AssistantMessageItem(
            content="Here's the quarterly data visualization."
        )
```

**Characteristics**:
- Custom UI components
- Real-time widget streaming
- Rich data presentation
- Interactive experiences

---

### Pattern 5: Production Server

**Use case**: Real applications, scalable systems, enterprise deployments

```python
from chatkit.server import ChatKitServer, stream_agent_response
from chatkit.stores import PostgresStore
from agents import Agent, Runner
import logging
import os

logger = logging.getLogger(__name__)

class ProductionServer(ChatKitServer):
    def __init__(self):
        # Production store with connection pooling
        data_store = PostgresStore(
            database_url=os.getenv("DATABASE_URL"),
            pool_size=20,
            max_overflow=10
        )

        # Optional attachment store
        attachment_store = BlobStorageStore(data_store)

        super().__init__(data_store, attachment_store)

    assistant = Agent(
        model="gpt-4o",
        name="ProductionAssistant",
        instructions="You are a production-ready assistant",
        tools=[],  # Add production tools
    )

    async def respond(self, thread, input, context):
        try:
            # Log request
            logger.info(f"Processing thread {thread.id}")

            # Validate input
            if not input or not input.content:
                yield AssistantMessageItem(
                    content="I didn't receive any input. How can I help?"
                )
                return

            # Process with agent
            result = Runner.run_streamed(self.assistant, [input])

            async for event in stream_agent_response(context, result):
                yield event

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            yield AssistantMessageItem(
                content="I encountered an error. Please try again or contact support."
            )
```

**Characteristics**:
- Persistent storage (PostgreSQL)
- Comprehensive error handling
- Logging and monitoring
- Connection pooling
- Attachment support
- Input validation

---

## Data Store Implementations

### MemoryStore

**Use case**: Development, testing, demos

```python
from chatkit.stores import MemoryStore

store = MemoryStore()
server = MyChatKitServer(store)
```

**Characteristics**:
- In-memory storage
- No setup required
- Data lost on restart
- Fast for development

**Limitations**:
- Not suitable for production
- No persistence
- Single-instance only

---

### PostgresStore

**Use case**: Production, multi-instance deployments

```python
from chatkit.stores import PostgresStore

store = PostgresStore(
    database_url="postgresql://user:pass@localhost:5432/chatkit",
    pool_size=20,
    max_overflow=10
)
server = MyChatKitServer(store)
```

**Setup**:
```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Set environment variable
export DATABASE_URL="postgresql://user:pass@localhost:5432/chatkit"

# Run migrations (if provided by ChatKit)
chatkit migrate
```

**Characteristics**:
- Persistent storage
- Scalable
- ACID compliance
- Connection pooling
- Multi-instance support

---

### Custom Store Implementation

**Use case**: Redis, MongoDB, custom databases

```python
from chatkit.stores import Store
from typing import List, Optional

class RedisStore(Store):
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def get_thread(self, thread_id: str) -> Optional[ThreadMetadata]:
        # Implementation
        pass

    async def save_thread(self, thread: ThreadMetadata) -> None:
        # Implementation
        pass

    async def get_messages(self, thread_id: str) -> List[MessageItem]:
        # Implementation
        pass

    async def save_message(self, thread_id: str, message: MessageItem) -> None:
        # Implementation
        pass
```

**Required Methods**:
- `get_thread(thread_id)`: Retrieve thread metadata
- `save_thread(thread)`: Persist thread metadata
- `get_messages(thread_id)`: Retrieve message history
- `save_message(thread_id, message)`: Persist message

---

## FastAPI Integration Patterns

### Basic Integration

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from chatkit.server import StreamingResult

app = FastAPI()
server = MyChatKitServer(MemoryStore())

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})

    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    else:
        return Response(content=result.json, media_type="application/json")
```

---

### With CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### With Dependency Injection

```python
from fastapi import Depends

def get_chatkit_server():
    return MyChatKitServer(PostgresStore())

@app.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    server: MyChatKitServer = Depends(get_chatkit_server)
):
    result = await server.process(await request.body(), {"request": request})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

---

### With Authentication

```python
from fastapi import HTTPException, Header

async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    # Verify token
    return token

@app.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    token: str = Depends(verify_token)
):
    # Pass user context to server
    result = await server.process(
        await request.body(),
        {"user_token": token, "request": request}
    )

    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

---

## Scaling Strategies

### Horizontal Scaling

**Requirements**:
- Persistent store (PostgreSQL, Redis)
- Stateless server instances
- Load balancer

**Architecture**:
```
Load Balancer
    ↓
[Server 1] [Server 2] [Server 3]
    ↓         ↓         ↓
    PostgreSQL Database
```

**Configuration**:
```python
# Each instance connects to shared database
store = PostgresStore(
    database_url=os.getenv("DATABASE_URL"),
    pool_size=10  # Per instance
)
```

---

### Vertical Scaling

**Optimize single instance**:

```python
# Increase connection pool
store = PostgresStore(
    database_url=os.getenv("DATABASE_URL"),
    pool_size=50,
    max_overflow=20
)

# Use async operations
async def respond(self, thread, input, context):
    # All I/O should be async
    result = await async_operation()
```

---

### Caching Strategy

```python
from functools import lru_cache
import redis

class CachedServer(ChatKitServer):
    def __init__(self, data_store):
        super().__init__(data_store)
        self.cache = redis.Redis()

    async def respond(self, thread, input, context):
        # Check cache
        cache_key = f"response:{input.content}"
        cached = self.cache.get(cache_key)

        if cached:
            yield AssistantMessageItem(content=cached.decode())
            return

        # Generate response
        result = await generate_response(input)

        # Cache result
        self.cache.setex(cache_key, 3600, result)

        yield AssistantMessageItem(content=result)
```

---

## Error Handling Patterns

### Graceful Degradation

```python
async def respond(self, thread, input, context):
    try:
        # Try primary agent
        result = Runner.run_streamed(self.primary_agent, [input])
        async for event in stream_agent_response(context, result):
            yield event
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
        # Fallback to simpler response
        yield AssistantMessageItem(
            content="I'm experiencing technical difficulties. Please try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        yield AssistantMessageItem(
            content="An error occurred. Please contact support."
        )
```

---

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class ResilientServer(ChatKitServer):
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def call_agent(self, input):
        return Runner.run_streamed(self.assistant, [input])

    async def respond(self, thread, input, context):
        try:
            result = await self.call_agent(input)
            async for event in stream_agent_response(context, result):
                yield event
        except Exception as e:
            logger.error(f"Failed after retries: {e}")
            yield AssistantMessageItem(content="Service temporarily unavailable")
```

---

## Monitoring and Observability

### Logging

```python
import logging
import time

logger = logging.getLogger(__name__)

class MonitoredServer(ChatKitServer):
    async def respond(self, thread, input, context):
        start_time = time.time()

        try:
            logger.info(f"Processing thread {thread.id}")

            result = Runner.run_streamed(self.assistant, [input])

            async for event in stream_agent_response(context, result):
                yield event

            duration = time.time() - start_time
            logger.info(f"Completed thread {thread.id} in {duration:.2f}s")

        except Exception as e:
            logger.error(f"Error in thread {thread.id}: {e}", exc_info=True)
            raise
```

---

### Metrics

```python
from prometheus_client import Counter, Histogram

request_counter = Counter('chatkit_requests_total', 'Total requests')
request_duration = Histogram('chatkit_request_duration_seconds', 'Request duration')

class MetricsServer(ChatKitServer):
    async def respond(self, thread, input, context):
        request_counter.inc()

        with request_duration.time():
            result = Runner.run_streamed(self.assistant, [input])
            async for event in stream_agent_response(context, result):
                yield event
```

---

## Security Considerations

### Input Validation

```python
async def respond(self, thread, input, context):
    # Validate input length
    if input and len(input.content) > 10000:
        yield AssistantMessageItem(
            content="Input too long. Please limit to 10,000 characters."
        )
        return

    # Sanitize input
    sanitized = sanitize_input(input.content)

    # Process
    result = Runner.run_streamed(self.assistant, [sanitized])
    async for event in stream_agent_response(context, result):
        yield event
```

---

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chatkit")
@limiter.limit("10/minute")
async def chatkit_endpoint(request: Request):
    # Process request
    pass
```

---

### Content Filtering

```python
async def respond(self, thread, input, context):
    # Check for inappropriate content
    if contains_inappropriate_content(input.content):
        yield AssistantMessageItem(
            content="I cannot process this request."
        )
        return

    # Process normally
    result = Runner.run_streamed(self.assistant, [input])
    async for event in stream_agent_response(context, result):
        yield event
```

---

## Design Decisions

### Why AsyncIterator for respond()?

**Enables streaming**: Yield events as they're generated, providing real-time updates to users.

**Memory efficient**: Don't need to buffer entire response before sending.

**Better UX**: Users see responses immediately, not after completion.

---

### Why Single /chatkit Endpoint?

**Simplicity**: One endpoint handles all ChatKit operations (messages, threads, tools).

**Protocol abstraction**: ChatKit protocol handles routing internally.

**Easier integration**: Frontend only needs to know one endpoint.

---

### Why Pluggable Stores?

**Flexibility**: Choose storage based on requirements (dev vs prod).

**Testability**: Use MemoryStore for tests, PostgresStore for production.

**Extensibility**: Implement custom stores for specific needs.

---

## Performance Optimization

### Connection Pooling

```python
store = PostgresStore(
    database_url=os.getenv("DATABASE_URL"),
    pool_size=20,  # Concurrent connections
    max_overflow=10,  # Additional connections under load
    pool_timeout=30,  # Wait time for connection
    pool_recycle=3600  # Recycle connections hourly
)
```

---

### Async Operations

```python
async def respond(self, thread, input, context):
    # Run operations concurrently
    results = await asyncio.gather(
        fetch_user_data(thread.user_id),
        fetch_context_data(thread.id),
        fetch_preferences(thread.user_id)
    )

    # Process with all data
    result = Runner.run_streamed(self.assistant, [input], context=results)
    async for event in stream_agent_response(context, result):
        yield event
```

---

### Response Caching

```python
from cachetools import TTLCache

class CachedServer(ChatKitServer):
    def __init__(self, data_store):
        super().__init__(data_store)
        self.cache = TTLCache(maxsize=1000, ttl=3600)

    async def respond(self, thread, input, context):
        cache_key = (thread.id, input.content)

        if cache_key in self.cache:
            yield self.cache[cache_key]
            return

        # Generate and cache
        result = await generate_response(input)
        self.cache[cache_key] = result
        yield result
```
