# ChatKit Server Quickstart

Complete working examples from hello world to production, with step-by-step setup instructions.

---

## Example 1: Hello World (5 minutes)

Simplest possible ChatKit server that echoes user input.

### Setup

```bash
# Create project directory
mkdir chatkit-hello-world
cd chatkit-hello-world

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install chatkit-python fastapi uvicorn
```

### Implementation

Create `main.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from chatkit.server import ChatKitServer, ThreadMetadata, UserMessageItem, StreamingResult
from chatkit.types import AssistantMessageItem
from chatkit.stores import MemoryStore
from typing import AsyncIterator, Any

# Define ChatKit server
class HelloWorldServer(ChatKitServer):
    def __init__(self):
        super().__init__(MemoryStore())

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator:
        if input:
            yield AssistantMessageItem(content=f"You said: {input.content}")
        else:
            yield AssistantMessageItem(content="Hello! Send me a message.")

# Initialize FastAPI
app = FastAPI(title="ChatKit Hello World")
server = HelloWorldServer()

# ChatKit endpoint
@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    else:
        return Response(content=result.json, media_type="application/json")

# Health check
@app.get("/")
async def root():
    return {"message": "ChatKit Hello World Server"}
```

### Run

```bash
uvicorn main:app --reload --port 8000
```

### Test

```bash
# In another terminal
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello ChatKit!"}'
```

**Expected**: Server echoes your message back.

---

## Example 2: AI-Powered Assistant (10 minutes)

Add OpenAI Agents SDK for intelligent conversations.

### Setup

```bash
# Install additional dependencies
pip install openai-agents-sdk

# Set API key
export OPENAI_API_KEY=sk-proj-...
```

### Implementation

Create `agent_server.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from chatkit.server import ChatKitServer, StreamingResult, stream_agent_response
from chatkit.stores import MemoryStore
from chatkit.helpers import simple_to_agent_input
from agents import Agent, Runner
from agents.context import AgentContext
import os

# Define agent
assistant_agent = Agent(
    model="gpt-4o",
    name="Assistant",
    instructions="You are a helpful assistant. Be concise and friendly."
)

# Define ChatKit server
class AgentServer(ChatKitServer):
    def __init__(self):
        super().__init__(MemoryStore())

    async def respond(self, thread, input, context):
        # Create agent context
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Convert input to agent format
        agent_input = await simple_to_agent_input(input) if input else []

        # Run agent with streaming
        result = Runner.run_streamed(
            assistant_agent,
            agent_input,
            context=agent_context,
        )

        # Stream events to client
        async for event in stream_agent_response(agent_context, result):
            yield event

# Initialize FastAPI
app = FastAPI(title="ChatKit Agent Server")
server = AgentServer()

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    else:
        return Response(content=result.json, media_type="application/json")

@app.get("/")
async def root():
    return {"message": "ChatKit Agent Server", "model": "gpt-4o"}
```

### Run

```bash
uvicorn agent_server:app --reload --port 8000
```

### Test

```bash
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'
```

**Expected**: AI-powered response about Paris.

---

## Example 3: Server with Tools (15 minutes)

Add custom function tools for external integrations.

### Implementation

Create `tool_server.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from chatkit.server import ChatKitServer, StreamingResult, stream_agent_response
from chatkit.stores import MemoryStore
from agents import Agent, Runner, function_tool
from agents.context import AgentContext
from chatkit.helpers import simple_to_agent_input
import datetime

# Define tools
@function_tool
def get_current_time() -> str:
    """Get the current time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Args:
        expression: Math expression like "2 + 2" or "10 * 5"
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@function_tool
def get_weather(location: str) -> str:
    """
    Get weather information for a location.

    Args:
        location: City name or location
    """
    # Mock implementation
    return f"Weather in {location}: Sunny, 72°F"

# Define agent with tools
assistant_agent = Agent(
    model="gpt-4o",
    name="ToolAssistant",
    instructions="""You are a helpful assistant with access to tools.
    Use the tools when appropriate to help users.
    - Use get_current_time when users ask about time
    - Use calculate for math problems
    - Use get_weather for weather information""",
    tools=[get_current_time, calculate, get_weather]
)

# Define ChatKit server
class ToolServer(ChatKitServer):
    def __init__(self):
        super().__init__(MemoryStore())

    async def respond(self, thread, input, context):
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        agent_input = await simple_to_agent_input(input) if input else []

        result = Runner.run_streamed(
            assistant_agent,
            agent_input,
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, result):
            yield event

# Initialize FastAPI
app = FastAPI(title="ChatKit Tool Server")
server = ToolServer()

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    else:
        return Response(content=result.json, media_type="application/json")

@app.get("/")
async def root():
    return {
        "message": "ChatKit Tool Server",
        "tools": ["get_current_time", "calculate", "get_weather"]
    }
```

### Run

```bash
uvicorn tool_server:app --reload --port 8000
```

### Test

```bash
# Test time tool
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it?"}'

# Test calculator tool
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate 15 * 23"}'

# Test weather tool
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in Tokyo?"}'
```

**Expected**: Agent uses appropriate tools to answer questions.

---

## Example 4: Production Server (30 minutes)

Full production setup with PostgreSQL, error handling, and monitoring.

### Setup

```bash
# Install production dependencies
pip install chatkit-python openai-agents-sdk fastapi uvicorn psycopg2-binary python-dotenv

# Install PostgreSQL (if not already installed)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql
# Windows: Download from postgresql.org

# Create database
createdb chatkit_production

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-proj-...
DATABASE_URL=postgresql://localhost/chatkit_production
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com
EOF
```

### Implementation

Create `production_server.py`:

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from chatkit.server import ChatKitServer, StreamingResult, stream_agent_response
from chatkit.stores import PostgresStore
from agents import Agent, Runner, function_tool
from agents.context import AgentContext
from chatkit.helpers import simple_to_agent_input
import logging
import os
from dotenv import load_dotenv
from typing import AsyncIterator, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define production tools
@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information."""
    # Production implementation would query actual database
    logger.info(f"Searching knowledge base: {query}")
    return f"Knowledge base results for: {query}"

# Define production agent
production_agent = Agent(
    model="gpt-4o",
    name="ProductionAssistant",
    instructions="""You are a production-ready assistant.
    - Be helpful and professional
    - Use tools when appropriate
    - Handle errors gracefully
    - Provide accurate information""",
    tools=[search_knowledge_base]
)

# Define production ChatKit server
class ProductionChatServer(ChatKitServer):
    def __init__(self):
        # Initialize PostgreSQL store
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        data_store = PostgresStore(
            database_url=database_url,
            pool_size=20,
            max_overflow=10
        )

        super().__init__(data_store)
        logger.info("Production ChatKit server initialized")

    async def respond(
        self,
        thread,
        input,
        context: Any,
    ) -> AsyncIterator:
        try:
            # Log request
            logger.info(f"Processing thread {thread.id}")

            # Validate input
            if input and len(input.content) > 10000:
                yield AssistantMessageItem(
                    content="Input too long. Please limit to 10,000 characters."
                )
                return

            # Create agent context
            agent_context = AgentContext(
                thread=thread,
                store=self.store,
                request_context=context,
            )

            # Convert input
            agent_input = await simple_to_agent_input(input) if input else []

            # Run agent
            result = Runner.run_streamed(
                production_agent,
                agent_input,
                context=agent_context,
            )

            # Stream events
            async for event in stream_agent_response(agent_context, result):
                yield event

            logger.info(f"Completed thread {thread.id}")

        except Exception as e:
            logger.error(f"Error processing thread {thread.id}: {e}", exc_info=True)
            yield AssistantMessageItem(
                content="I encountered an error. Please try again or contact support."
            )

# Initialize FastAPI
app = FastAPI(
    title="ChatKit Production Server",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize server
try:
    server = ProductionChatServer()
except Exception as e:
    logger.error(f"Failed to initialize server: {e}")
    raise

# ChatKit endpoint
@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    try:
        result = await server.process(
            await request.body(),
            {"request": request}
        )

        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        else:
            return Response(content=result.json, media_type="application/json")

    except Exception as e:
        logger.error(f"Error in chatkit endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected"
    }

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return {
        "requests_total": 0,  # Implement actual metrics
        "errors_total": 0,
        "avg_response_time": 0
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("ChatKit Production Server starting up")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("ChatKit Production Server shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
```

### Run

```bash
# Development
uvicorn production_server:app --reload --port 8000

# Production
uvicorn production_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Test

```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -d '{"message": "Search for information about ChatKit"}'

# Metrics
curl http://localhost:8000/metrics
```

---

## Example 5: Multi-Agent System (Advanced)

Multiple specialized agents working together.

### Implementation

Create `multi_agent_server.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from chatkit.server import ChatKitServer, StreamingResult, stream_agent_response
from chatkit.stores import MemoryStore
from agents import Agent, Runner, function_tool
from agents.context import AgentContext
from chatkit.helpers import simple_to_agent_input

# Define specialized agents
code_agent = Agent(
    model="gpt-4o",
    name="CodeExpert",
    instructions="You are a coding expert. Help with programming questions."
)

math_agent = Agent(
    model="gpt-4o",
    name="MathExpert",
    instructions="You are a math expert. Help with mathematical problems."
)

general_agent = Agent(
    model="gpt-4o",
    name="GeneralAssistant",
    instructions="You are a general assistant. Help with various questions."
)

# Router agent
router_agent = Agent(
    model="gpt-4o",
    name="Router",
    instructions="""You are a routing agent. Analyze the user's question and determine which expert to use:
    - Use CodeExpert for programming, coding, software questions
    - Use MathExpert for math, calculations, equations
    - Use GeneralAssistant for everything else

    Respond with just the agent name: CodeExpert, MathExpert, or GeneralAssistant"""
)

class MultiAgentServer(ChatKitServer):
    def __init__(self):
        super().__init__(MemoryStore())

    async def respond(self, thread, input, context):
        if not input:
            yield AssistantMessageItem(content="How can I help you?")
            return

        # Route to appropriate agent
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Determine which agent to use
        routing_result = Runner.run_streamed(
            router_agent,
            [{"role": "user", "content": f"Route this: {input.content}"}],
            context=agent_context,
        )

        # Get routing decision
        route = None
        async for event in routing_result:
            if hasattr(event, 'content'):
                route = event.content.strip()
                break

        # Select agent
        if "CodeExpert" in route:
            selected_agent = code_agent
        elif "MathExpert" in route:
            selected_agent = math_agent
        else:
            selected_agent = general_agent

        # Run selected agent
        agent_input = await simple_to_agent_input(input)
        result = Runner.run_streamed(
            selected_agent,
            agent_input,
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, result):
            yield event

# Initialize FastAPI
app = FastAPI(title="ChatKit Multi-Agent Server")
server = MultiAgentServer()

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    else:
        return Response(content=result.json, media_type="application/json")
```

---

## Deployment Patterns

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "production_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  chatkit-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/chatkit
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=chatkit
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run:
```bash
docker-compose up
```

---

### Cloud Deployment (Railway)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
```

---

### Cloud Deployment (Render)

Create `render.yaml`:

```yaml
services:
  - type: web
    name: chatkit-server
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn production_server:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: chatkit-db
          property: connectionString

databases:
  - name: chatkit-db
    plan: starter
```

---

## Testing

### Unit Tests

Create `test_server.py`:

```python
import pytest
from chatkit.server import ChatKitServer
from chatkit.stores import MemoryStore
from chatkit.types import ThreadMetadata, UserMessageItem

@pytest.mark.asyncio
async def test_echo_server():
    class TestServer(ChatKitServer):
        def __init__(self):
            super().__init__(MemoryStore())

        async def respond(self, thread, input, context):
            if input:
                yield AssistantMessageItem(content=f"Echo: {input.content}")

    server = TestServer()
    thread = ThreadMetadata(id="test-thread")
    input_msg = UserMessageItem(content="Hello")

    events = []
    async for event in server.respond(thread, input_msg, {}):
        events.append(event)

    assert len(events) == 1
    assert "Echo: Hello" in events[0].content
```

Run tests:
```bash
pytest test_server.py
```

---

## Troubleshooting

### Issue: Server not starting

**Check**:
```bash
# Verify dependencies
pip list | grep chatkit

# Check Python version
python --version  # Should be 3.11+

# Check environment variables
echo $OPENAI_API_KEY
```

### Issue: Database connection errors

**Check**:
```bash
# Test database connection
psql $DATABASE_URL

# Verify database exists
psql -l | grep chatkit
```

### Issue: Streaming not working

**Verify**:
- Using `StreamingResponse` with `media_type="text/event-stream"`
- Not buffering responses
- Client supports SSE

### Issue: Agent not responding

**Check**:
```bash
# Verify API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check logs
tail -f server.log
```
