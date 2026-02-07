# OpenAI Agents SDK Integration

Comprehensive guide to integrating OpenAI Agents SDK with ChatKit Server.

---

## Overview

ChatKit Server provides seamless integration with OpenAI Agents SDK through helper functions that convert agent runs into ChatKit events.

**Key Helper**: `stream_agent_response()` - Converts streamed Agents SDK runs into ChatKit `ThreadStreamEvent` objects.

---

## Basic Integration Pattern

### Minimal Agent Integration

```python
from chatkit.server import ChatKitServer, stream_agent_response
from chatkit.stores import MemoryStore
from chatkit.helpers import simple_to_agent_input
from agents import Agent, Runner
from agents.context import AgentContext

class BasicAgentServer(ChatKitServer):
    def __init__(self):
        super().__init__(MemoryStore())

    # Define agent as class attribute
    assistant = Agent(
        model="gpt-4o",
        name="Assistant",
        instructions="You are a helpful assistant"
    )

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
            self.assistant,
            agent_input,
            context=agent_context,
        )

        # Stream events to ChatKit
        async for event in stream_agent_response(agent_context, result):
            yield event
```

---

## Agent Configuration

### Model Selection

```python
# GPT-4o (recommended for production)
agent = Agent(
    model="gpt-4o",
    name="Assistant",
    instructions="You are a helpful assistant"
)

# GPT-4o-mini (faster, cheaper)
agent = Agent(
    model="gpt-4o-mini",
    name="QuickAssistant",
    instructions="You are a quick assistant"
)

# GPT-4 Turbo
agent = Agent(
    model="gpt-4-turbo",
    name="TurboAssistant",
    instructions="You are a turbo assistant"
)
```

---

### Instructions

**Best Practices**:
- Be specific and clear
- Define personality and tone
- Specify constraints and limitations
- Include examples when helpful

```python
agent = Agent(
    model="gpt-4o",
    name="CustomerSupport",
    instructions="""You are a customer support assistant for TechCorp.

    Personality:
    - Professional and friendly
    - Patient and empathetic
    - Solution-oriented

    Guidelines:
    - Always greet users warmly
    - Ask clarifying questions when needed
    - Provide step-by-step solutions
    - Escalate to human agent if unable to help

    Constraints:
    - Do not make promises about refunds (escalate to human)
    - Do not share internal company information
    - Keep responses concise (under 200 words)

    Example interactions:
    User: "My order hasn't arrived"
    You: "I'm sorry to hear that. Let me help you track your order. Could you provide your order number?"
    """
)
```

---

### Temperature and Parameters

```python
agent = Agent(
    model="gpt-4o",
    name="CreativeWriter",
    instructions="You are a creative writing assistant",
    temperature=0.9,  # Higher for creativity (0.0-2.0)
    max_tokens=1000,  # Limit response length
    top_p=0.95,       # Nucleus sampling
)

# For factual/deterministic responses
factual_agent = Agent(
    model="gpt-4o",
    name="FactChecker",
    instructions="Provide accurate, factual information",
    temperature=0.1,  # Lower for consistency
)
```

---

## Context Management

### AgentContext

Provides agents with access to conversation state and storage.

```python
from agents.context import AgentContext

async def respond(self, thread, input, context):
    # Create agent context with full state
    agent_context = AgentContext(
        thread=thread,              # Thread metadata
        store=self.store,           # Data store for persistence
        request_context=context,    # Request-specific context
    )

    # Pass to agent
    result = Runner.run_streamed(
        self.assistant,
        agent_input,
        context=agent_context,
    )

    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

### Custom Context Data

```python
async def respond(self, thread, input, context):
    # Add custom data to context
    custom_context = {
        "user_id": context.get("user_id"),
        "session_id": context.get("session_id"),
        "preferences": await self.get_user_preferences(context.get("user_id")),
        "history": await self.get_conversation_history(thread.id),
    }

    agent_context = AgentContext(
        thread=thread,
        store=self.store,
        request_context=custom_context,
    )

    # Agent can access custom_context during execution
    result = Runner.run_streamed(
        self.assistant,
        agent_input,
        context=agent_context,
    )

    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

## Input Conversion

### simple_to_agent_input Helper

Converts ChatKit `UserMessageItem` to Agents SDK format.

```python
from chatkit.helpers import simple_to_agent_input

async def respond(self, thread, input, context):
    # Convert single message
    agent_input = await simple_to_agent_input(input) if input else []

    # agent_input is now in format: [{"role": "user", "content": "..."}]
```

---

### Manual Input Formatting

```python
async def respond(self, thread, input, context):
    # Manual formatting for complex inputs
    agent_input = []

    if input:
        # Add system message
        agent_input.append({
            "role": "system",
            "content": "Additional context for this request"
        })

        # Add user message
        agent_input.append({
            "role": "user",
            "content": input.content
        })

        # Add images if present
        if hasattr(input, 'images') and input.images:
            agent_input.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": input.content},
                    {"type": "image_url", "image_url": {"url": input.images[0]}}
                ]
            })

    result = Runner.run_streamed(self.assistant, agent_input, context=agent_context)
    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

## Event Streaming

### stream_agent_response Helper

Converts Agents SDK events to ChatKit events.

```python
from chatkit.server import stream_agent_response

async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    result = Runner.run_streamed(self.assistant, agent_input, context=agent_context)

    # stream_agent_response handles:
    # - Message chunks → AssistantMessageItem
    # - Tool calls → ToolCallEvent
    # - Tool results → ToolResultEvent
    # - Errors → ErrorEvent
    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

### Custom Event Processing

```python
async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    result = Runner.run_streamed(self.assistant, agent_input, context=agent_context)

    async for event in stream_agent_response(agent_context, result):
        # Intercept and modify events
        if isinstance(event, AssistantMessageItem):
            # Add metadata
            event.metadata = {"processed_at": datetime.now().isoformat()}

        # Filter events
        if should_send_event(event):
            yield event
```

---

## Multi-Agent Patterns

### Sequential Agents

Run multiple agents in sequence.

```python
class SequentialAgentServer(ChatKitServer):
    analyzer = Agent(
        model="gpt-4o",
        name="Analyzer",
        instructions="Analyze the user's request and extract key information"
    )

    responder = Agent(
        model="gpt-4o",
        name="Responder",
        instructions="Provide a helpful response based on the analysis"
    )

    async def respond(self, thread, input, context):
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

        # Step 1: Analyze
        analysis_result = Runner.run_streamed(
            self.analyzer,
            [{"role": "user", "content": input.content}],
            context=agent_context,
        )

        analysis = ""
        async for event in analysis_result:
            if hasattr(event, 'content'):
                analysis += event.content

        # Step 2: Respond based on analysis
        response_input = [
            {"role": "system", "content": f"Analysis: {analysis}"},
            {"role": "user", "content": input.content}
        ]

        response_result = Runner.run_streamed(
            self.responder,
            response_input,
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, response_result):
            yield event
```

---

### Parallel Agents

Run multiple agents concurrently and combine results.

```python
import asyncio

class ParallelAgentServer(ChatKitServer):
    fact_checker = Agent(
        model="gpt-4o",
        name="FactChecker",
        instructions="Verify factual accuracy"
    )

    sentiment_analyzer = Agent(
        model="gpt-4o",
        name="SentimentAnalyzer",
        instructions="Analyze sentiment and tone"
    )

    async def respond(self, thread, input, context):
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

        # Run agents in parallel
        fact_task = asyncio.create_task(
            self.run_agent(self.fact_checker, input, agent_context)
        )
        sentiment_task = asyncio.create_task(
            self.run_agent(self.sentiment_analyzer, input, agent_context)
        )

        # Wait for both
        fact_result, sentiment_result = await asyncio.gather(fact_task, sentiment_task)

        # Combine results
        combined = f"Facts: {fact_result}\n\nSentiment: {sentiment_result}"
        yield AssistantMessageItem(content=combined)

    async def run_agent(self, agent, input, context):
        result = Runner.run_streamed(agent, [{"role": "user", "content": input.content}], context=context)
        output = ""
        async for event in result:
            if hasattr(event, 'content'):
                output += event.content
        return output
```

---

### Conditional Agents

Route to different agents based on conditions.

```python
class ConditionalAgentServer(ChatKitServer):
    technical_agent = Agent(
        model="gpt-4o",
        name="TechnicalSupport",
        instructions="Provide technical support"
    )

    billing_agent = Agent(
        model="gpt-4o",
        name="BillingSupport",
        instructions="Handle billing questions"
    )

    general_agent = Agent(
        model="gpt-4o",
        name="GeneralSupport",
        instructions="Handle general inquiries"
    )

    async def respond(self, thread, input, context):
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

        # Determine which agent to use
        content_lower = input.content.lower()

        if any(word in content_lower for word in ["bug", "error", "crash", "technical"]):
            selected_agent = self.technical_agent
        elif any(word in content_lower for word in ["billing", "payment", "invoice", "charge"]):
            selected_agent = self.billing_agent
        else:
            selected_agent = self.general_agent

        # Run selected agent
        result = Runner.run_streamed(
            selected_agent,
            await simple_to_agent_input(input),
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, result):
            yield event
```

---

## Memory and State

### Conversation History

Agents automatically access conversation history through `AgentContext`.

```python
async def respond(self, thread, input, context):
    agent_context = AgentContext(
        thread=thread,
        store=self.store,  # Store contains conversation history
        request_context=context,
    )

    # Agent automatically has access to previous messages in thread
    result = Runner.run_streamed(
        self.assistant,
        await simple_to_agent_input(input),
        context=agent_context,
    )

    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

### Custom Memory

```python
class MemoryAgentServer(ChatKitServer):
    def __init__(self, data_store):
        super().__init__(data_store)
        self.user_memory = {}  # In-memory cache

    async def respond(self, thread, input, context):
        user_id = context.get("user_id")

        # Load user memory
        if user_id not in self.user_memory:
            self.user_memory[user_id] = await self.load_user_memory(user_id)

        # Add memory to context
        memory_context = {
            **context,
            "user_memory": self.user_memory[user_id]
        }

        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=memory_context,
        )

        # Agent can access user_memory through context
        result = Runner.run_streamed(
            self.assistant,
            await simple_to_agent_input(input),
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, result):
            yield event

        # Update memory after response
        await self.save_user_memory(user_id, self.user_memory[user_id])

    async def load_user_memory(self, user_id):
        # Load from database
        return {"preferences": {}, "history": []}

    async def save_user_memory(self, user_id, memory):
        # Save to database
        pass
```

---

## Error Handling

### Agent Errors

```python
from agents.exceptions import AgentError, ModelError

async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    try:
        result = Runner.run_streamed(
            self.assistant,
            await simple_to_agent_input(input),
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, result):
            yield event

    except ModelError as e:
        logger.error(f"Model error: {e}")
        yield AssistantMessageItem(
            content="I'm having trouble connecting to the AI service. Please try again."
        )

    except AgentError as e:
        logger.error(f"Agent error: {e}")
        yield AssistantMessageItem(
            content="I encountered an error processing your request. Please try again."
        )

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        yield AssistantMessageItem(
            content="An unexpected error occurred. Please contact support."
        )
```

---

### Timeout Handling

```python
import asyncio

async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    try:
        result = Runner.run_streamed(
            self.assistant,
            await simple_to_agent_input(input),
            context=agent_context,
        )

        # Set timeout for agent response
        async with asyncio.timeout(30):  # 30 second timeout
            async for event in stream_agent_response(agent_context, result):
                yield event

    except asyncio.TimeoutError:
        logger.error("Agent response timeout")
        yield AssistantMessageItem(
            content="The request is taking longer than expected. Please try again."
        )
```

---

## Performance Optimization

### Agent Caching

```python
from functools import lru_cache

class CachedAgentServer(ChatKitServer):
    @lru_cache(maxsize=10)
    def get_agent(self, agent_type: str) -> Agent:
        """Cache agent instances"""
        if agent_type == "technical":
            return Agent(model="gpt-4o", name="Technical", instructions="...")
        elif agent_type == "billing":
            return Agent(model="gpt-4o", name="Billing", instructions="...")
        else:
            return Agent(model="gpt-4o", name="General", instructions="...")

    async def respond(self, thread, input, context):
        agent_type = self.determine_agent_type(input)
        agent = self.get_agent(agent_type)

        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

        result = Runner.run_streamed(agent, await simple_to_agent_input(input), context=agent_context)

        async for event in stream_agent_response(agent_context, result):
            yield event
```

---

### Batch Processing

```python
async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    # Batch multiple operations
    operations = [
        self.preprocess_input(input),
        self.load_context(thread.id),
        self.check_permissions(context.get("user_id"))
    ]

    # Run in parallel
    processed_input, thread_context, permissions = await asyncio.gather(*operations)

    if not permissions:
        yield AssistantMessageItem(content="Permission denied")
        return

    # Run agent with preprocessed data
    result = Runner.run_streamed(
        self.assistant,
        processed_input,
        context=agent_context,
    )

    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

## Best Practices

### 1. Agent Design

- **Single Responsibility**: Each agent should have one clear purpose
- **Clear Instructions**: Be specific about agent behavior and constraints
- **Appropriate Model**: Use gpt-4o for complex tasks, gpt-4o-mini for simple ones
- **Temperature**: Lower (0.1-0.3) for factual, higher (0.7-0.9) for creative

### 2. Context Management

- **Minimal Context**: Only include necessary information
- **Structured Data**: Use typed objects, not raw strings
- **Cache When Possible**: Avoid redundant database queries
- **Clean Up**: Remove sensitive data after use

### 3. Error Handling

- **Graceful Degradation**: Provide fallback responses
- **User-Friendly Messages**: Don't expose technical details
- **Comprehensive Logging**: Log all errors with context
- **Retry Logic**: Implement for transient failures

### 4. Performance

- **Stream Responses**: Use streaming for better UX
- **Parallel Operations**: Run independent tasks concurrently
- **Cache Agents**: Reuse agent instances when possible
- **Timeout Protection**: Set reasonable timeouts

### 5. Security

- **Input Validation**: Sanitize all user input
- **Permission Checks**: Verify user authorization
- **Rate Limiting**: Prevent abuse
- **Audit Logging**: Track all agent interactions
