# Tools and Widgets

Advanced features for ChatKit Server: custom tools, widgets, and rich interactions.

---

## Custom Function Tools

### Basic Tool Definition

Use `@function_tool` decorator to create tools that agents can call.

```python
from agents import function_tool

@function_tool
def get_current_weather(location: str) -> str:
    """
    Get the current weather for a location.

    Args:
        location: City name or location string
    """
    # Implementation
    return f"Weather in {location}: Sunny, 72°F"
```

**Key Requirements**:
- Docstring with description (used by AI to understand tool)
- Type hints for parameters and return value
- Clear parameter descriptions in docstring

---

### Tool with Multiple Parameters

```python
@function_tool
def search_products(
    query: str,
    category: str | None = None,
    max_results: int = 10,
    sort_by: str = "relevance"
) -> list[dict]:
    """
    Search for products in the catalog.

    Args:
        query: Search query string
        category: Optional category filter (e.g., "electronics", "clothing")
        max_results: Maximum number of results to return (default: 10)
        sort_by: Sort order - "relevance", "price_low", "price_high" (default: "relevance")

    Returns:
        List of product dictionaries with id, name, price, and description
    """
    # Implementation
    results = [
        {"id": 1, "name": "Product A", "price": 29.99, "description": "..."},
        {"id": 2, "name": "Product B", "price": 49.99, "description": "..."},
    ]
    return results[:max_results]
```

---

### Tool with Complex Return Types

```python
from typing import TypedDict

class UserInfo(TypedDict):
    id: str
    name: str
    email: str
    role: str
    created_at: str

@function_tool
def get_user_info(user_id: str) -> UserInfo:
    """
    Get detailed information about a user.

    Args:
        user_id: The unique user identifier

    Returns:
        User information including id, name, email, role, and creation date
    """
    # Implementation
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "role": "admin",
        "created_at": "2024-01-15T10:30:00Z"
    }
```

---

### Async Tools

```python
@function_tool
async def fetch_external_data(api_endpoint: str) -> dict:
    """
    Fetch data from an external API.

    Args:
        api_endpoint: The API endpoint URL

    Returns:
        JSON response from the API
    """
    import httpx

    async with httpx.AsyncClient() as client:
        response = await client.get(api_endpoint)
        return response.json()
```

---

## Tool Integration Patterns

### Pattern 1: Basic Tool Integration

```python
from agents import Agent, function_tool

@function_tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

class ToolServer(ChatKitServer):
    assistant = Agent(
        model="gpt-4o",
        name="Assistant",
        instructions="You are a helpful assistant with access to a calculator",
        tools=[calculate]  # Register tool
    )

    async def respond(self, thread, input, context):
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)
        result = Runner.run_streamed(self.assistant, await simple_to_agent_input(input), context=agent_context)
        async for event in stream_agent_response(agent_context, result):
            yield event
```

---

### Pattern 2: Multiple Tools

```python
@function_tool
def search_database(query: str) -> list[dict]:
    """Search the knowledge database."""
    return [{"id": 1, "title": "Result 1", "content": "..."}]

@function_tool
def get_user_preferences(user_id: str) -> dict:
    """Get user preferences."""
    return {"theme": "dark", "language": "en"}

@function_tool
def send_notification(user_id: str, message: str) -> bool:
    """Send a notification to a user."""
    # Implementation
    return True

class MultiToolServer(ChatKitServer):
    assistant = Agent(
        model="gpt-4o",
        name="Assistant",
        instructions="""You are a helpful assistant with access to multiple tools:
        - search_database: Search for information
        - get_user_preferences: Get user settings
        - send_notification: Send notifications to users

        Use tools appropriately based on user requests.""",
        tools=[search_database, get_user_preferences, send_notification]
    )
```

---

### Pattern 3: Context-Aware Tools

Tools that access request context.

```python
from agents import function_tool

# Store context in a way tools can access
_request_context = {}

@function_tool
def get_current_user_info() -> dict:
    """Get information about the current user."""
    user_id = _request_context.get("user_id")
    if not user_id:
        return {"error": "No user context available"}

    # Fetch user info
    return {"id": user_id, "name": "John Doe"}

class ContextAwareToolServer(ChatKitServer):
    async def respond(self, thread, input, context):
        # Make context available to tools
        global _request_context
        _request_context = context

        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

        result = Runner.run_streamed(
            self.assistant,
            await simple_to_agent_input(input),
            context=agent_context
        )

        async for event in stream_agent_response(agent_context, result):
            yield event

        # Clean up
        _request_context = {}
```

---

### Pattern 4: Tool Error Handling

```python
@function_tool
def risky_operation(param: str) -> str:
    """
    Perform a risky operation that might fail.

    Args:
        param: Operation parameter

    Returns:
        Success message or error description
    """
    try:
        # Risky operation
        if not param:
            raise ValueError("Parameter cannot be empty")

        result = perform_operation(param)
        return f"Success: {result}"

    except ValueError as e:
        return f"Validation error: {str(e)}"

    except Exception as e:
        logger.error(f"Tool error: {e}", exc_info=True)
        return f"Operation failed: {str(e)}"
```

---

## Widget Streaming

### Basic Widget

```python
from chatkit.types import WidgetEvent

async def respond(self, thread, input, context):
    # Stream a widget
    yield WidgetEvent(
        widget_type="chart",
        data={
            "type": "bar",
            "title": "Sales Data",
            "values": [100, 200, 150, 300],
            "labels": ["Q1", "Q2", "Q3", "Q4"]
        }
    )

    # Stream explanation
    yield AssistantMessageItem(content="Here's your sales data visualization.")
```

---

### Multiple Widgets

```python
async def respond(self, thread, input, context):
    # Widget 1: Chart
    yield WidgetEvent(
        widget_type="chart",
        data={"type": "line", "values": [1, 2, 3, 4]}
    )

    # Message
    yield AssistantMessageItem(content="Here's the trend chart.")

    # Widget 2: Table
    yield WidgetEvent(
        widget_type="table",
        data={
            "headers": ["Name", "Value", "Status"],
            "rows": [
                ["Item 1", "100", "Active"],
                ["Item 2", "200", "Pending"]
            ]
        }
    )

    # Final message
    yield AssistantMessageItem(content="And here's the detailed data table.")
```

---

### Dynamic Widgets

```python
async def respond(self, thread, input, context):
    # Analyze request
    if "chart" in input.content.lower():
        widget_type = "chart"
        data = self.generate_chart_data(input.content)
    elif "table" in input.content.lower():
        widget_type = "table"
        data = self.generate_table_data(input.content)
    elif "map" in input.content.lower():
        widget_type = "map"
        data = self.generate_map_data(input.content)
    else:
        # Default to text response
        yield AssistantMessageItem(content="What type of visualization would you like?")
        return

    # Stream widget
    yield WidgetEvent(widget_type=widget_type, data=data)
    yield AssistantMessageItem(content=f"Here's your {widget_type}.")
```

---

### Interactive Widgets

```python
async def respond(self, thread, input, context):
    # Widget with interactive elements
    yield WidgetEvent(
        widget_type="form",
        data={
            "title": "User Feedback",
            "fields": [
                {
                    "type": "text",
                    "name": "name",
                    "label": "Your Name",
                    "required": True
                },
                {
                    "type": "select",
                    "name": "rating",
                    "label": "Rating",
                    "options": ["1", "2", "3", "4", "5"]
                },
                {
                    "type": "textarea",
                    "name": "comments",
                    "label": "Comments"
                }
            ],
            "submit_label": "Submit Feedback"
        }
    )

    yield AssistantMessageItem(content="Please fill out the feedback form.")
```

---

## Widget Types

### Chart Widget

```python
# Bar chart
yield WidgetEvent(
    widget_type="chart",
    data={
        "type": "bar",
        "title": "Monthly Revenue",
        "values": [10000, 15000, 12000, 18000],
        "labels": ["Jan", "Feb", "Mar", "Apr"],
        "color": "#4CAF50"
    }
)

# Line chart
yield WidgetEvent(
    widget_type="chart",
    data={
        "type": "line",
        "title": "User Growth",
        "datasets": [
            {
                "label": "Users",
                "values": [100, 150, 200, 300],
                "color": "#2196F3"
            },
            {
                "label": "Active Users",
                "values": [80, 120, 160, 240],
                "color": "#FF9800"
            }
        ],
        "labels": ["Week 1", "Week 2", "Week 3", "Week 4"]
    }
)

# Pie chart
yield WidgetEvent(
    widget_type="chart",
    data={
        "type": "pie",
        "title": "Market Share",
        "values": [30, 25, 20, 15, 10],
        "labels": ["Product A", "Product B", "Product C", "Product D", "Others"],
        "colors": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
    }
)
```

---

### Table Widget

```python
yield WidgetEvent(
    widget_type="table",
    data={
        "title": "User List",
        "headers": ["ID", "Name", "Email", "Status", "Actions"],
        "rows": [
            ["1", "John Doe", "john@example.com", "Active", "Edit | Delete"],
            ["2", "Jane Smith", "jane@example.com", "Pending", "Edit | Delete"],
            ["3", "Bob Johnson", "bob@example.com", "Active", "Edit | Delete"]
        ],
        "sortable": True,
        "filterable": True,
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total": 100
        }
    }
)
```

---

### Card Widget

```python
yield WidgetEvent(
    widget_type="card",
    data={
        "title": "User Profile",
        "image": "https://example.com/avatar.jpg",
        "fields": [
            {"label": "Name", "value": "John Doe"},
            {"label": "Email", "value": "john@example.com"},
            {"label": "Role", "value": "Administrator"},
            {"label": "Member Since", "value": "January 2024"}
        ],
        "actions": [
            {"label": "Edit Profile", "action": "edit"},
            {"label": "View Activity", "action": "activity"}
        ]
    }
)
```

---

### Map Widget

```python
yield WidgetEvent(
    widget_type="map",
    data={
        "center": {"lat": 37.7749, "lng": -122.4194},
        "zoom": 12,
        "markers": [
            {
                "lat": 37.7749,
                "lng": -122.4194,
                "title": "San Francisco",
                "description": "City by the Bay"
            },
            {
                "lat": 37.8044,
                "lng": -122.2712,
                "title": "Oakland",
                "description": "East Bay"
            }
        ]
    }
)
```

---

### Image Gallery Widget

```python
yield WidgetEvent(
    widget_type="gallery",
    data={
        "title": "Product Images",
        "images": [
            {
                "url": "https://example.com/image1.jpg",
                "thumbnail": "https://example.com/thumb1.jpg",
                "caption": "Product view 1"
            },
            {
                "url": "https://example.com/image2.jpg",
                "thumbnail": "https://example.com/thumb2.jpg",
                "caption": "Product view 2"
            }
        ],
        "layout": "grid"
    }
)
```

---

## File Attachments

### Attachment Store Setup

```python
from chatkit.stores import PostgresStore, BlobStorageStore

# Initialize stores
data_store = PostgresStore(database_url=os.getenv("DATABASE_URL"))
attachment_store = BlobStorageStore(data_store)

# Create server with attachment support
server = MyChatKitServer(data_store, attachment_store)
```

---

### Handling File Uploads

```python
async def respond(self, thread, input, context):
    # Check for attachments
    if hasattr(input, 'attachments') and input.attachments:
        for attachment in input.attachments:
            # Process attachment
            file_type = attachment.content_type
            file_name = attachment.filename
            file_data = attachment.data

            if file_type.startswith('image/'):
                # Process image
                result = await self.process_image(file_data)
                yield AssistantMessageItem(content=f"Processed image: {file_name}")

            elif file_type == 'application/pdf':
                # Process PDF
                text = await self.extract_pdf_text(file_data)
                yield AssistantMessageItem(content=f"Extracted text from {file_name}")

            elif file_type.startswith('text/'):
                # Process text file
                content = file_data.decode('utf-8')
                yield AssistantMessageItem(content=f"Read {len(content)} characters from {file_name}")

    # Continue with normal processing
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)
    result = Runner.run_streamed(self.assistant, await simple_to_agent_input(input), context=agent_context)
    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

### Sending File Responses

```python
from chatkit.types import AttachmentItem

async def respond(self, thread, input, context):
    # Generate file
    file_data = self.generate_report()

    # Send as attachment
    yield AttachmentItem(
        filename="report.pdf",
        content_type="application/pdf",
        data=file_data
    )

    yield AssistantMessageItem(content="Here's your report.")
```

---

## Advanced Patterns

### Pattern: Tool + Widget Combination

```python
@function_tool
def analyze_sales_data(period: str) -> dict:
    """Analyze sales data for a given period."""
    return {
        "total_sales": 50000,
        "growth": 15.5,
        "top_products": ["Product A", "Product B"],
        "chart_data": {
            "values": [10000, 12000, 13000, 15000],
            "labels": ["Week 1", "Week 2", "Week 3", "Week 4"]
        }
    }

class AnalyticsServer(ChatKitServer):
    assistant = Agent(
        model="gpt-4o",
        name="AnalyticsAssistant",
        instructions="Analyze data and provide visualizations",
        tools=[analyze_sales_data]
    )

    async def respond(self, thread, input, context):
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

        result = Runner.run_streamed(
            self.assistant,
            await simple_to_agent_input(input),
            context=agent_context
        )

        async for event in stream_agent_response(agent_context, result):
            # Intercept tool results
            if isinstance(event, ToolResultEvent):
                tool_result = event.result

                # If tool returned chart data, create widget
                if "chart_data" in tool_result:
                    yield WidgetEvent(
                        widget_type="chart",
                        data={
                            "type": "bar",
                            "values": tool_result["chart_data"]["values"],
                            "labels": tool_result["chart_data"]["labels"]
                        }
                    )

            yield event
```

---

### Pattern: Progressive Widget Updates

```python
async def respond(self, thread, input, context):
    # Initial widget (loading state)
    widget_id = "progress-widget-1"
    yield WidgetEvent(
        widget_type="progress",
        widget_id=widget_id,
        data={"status": "loading", "progress": 0}
    )

    # Process in steps
    for i, step in enumerate(["Analyzing", "Processing", "Generating"]):
        await asyncio.sleep(1)  # Simulate work

        # Update widget
        yield WidgetEvent(
            widget_type="progress",
            widget_id=widget_id,
            data={
                "status": step,
                "progress": (i + 1) * 33
            }
        )

    # Final result
    yield WidgetEvent(
        widget_type="result",
        data={"status": "complete", "result": "..."}
    )

    yield AssistantMessageItem(content="Processing complete!")
```

---

### Pattern: Conditional Widgets

```python
async def respond(self, thread, input, context):
    # Analyze request
    request_type = self.classify_request(input.content)

    if request_type == "data_visualization":
        # Return chart widget
        data = await self.fetch_data()
        yield WidgetEvent(
            widget_type="chart",
            data={"type": "bar", "values": data}
        )

    elif request_type == "user_lookup":
        # Return card widget
        user = await self.lookup_user(input.content)
        yield WidgetEvent(
            widget_type="card",
            data={"title": user["name"], "fields": user}
        )

    elif request_type == "location_query":
        # Return map widget
        location = await self.geocode(input.content)
        yield WidgetEvent(
            widget_type="map",
            data={"center": location, "zoom": 15}
        )

    else:
        # Default text response
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)
        result = Runner.run_streamed(self.assistant, await simple_to_agent_input(input), context=agent_context)
        async for event in stream_agent_response(agent_context, result):
            yield event
```

---

## Best Practices

### Tool Design

1. **Clear Documentation**: Write detailed docstrings
2. **Type Safety**: Use type hints for all parameters
3. **Error Handling**: Return error messages, don't raise exceptions
4. **Idempotency**: Tools should be safe to call multiple times
5. **Performance**: Keep tools fast (<2 seconds)

### Widget Design

1. **Responsive**: Design for mobile and desktop
2. **Accessible**: Include proper labels and ARIA attributes
3. **Progressive**: Show loading states for async operations
4. **Consistent**: Use consistent styling across widgets
5. **Lightweight**: Keep data payloads small

### Security

1. **Input Validation**: Validate all tool parameters
2. **Permission Checks**: Verify user authorization
3. **Rate Limiting**: Prevent tool abuse
4. **Sanitization**: Clean user input before processing
5. **Audit Logging**: Log all tool calls

### Performance

1. **Async Operations**: Use async for I/O operations
2. **Caching**: Cache expensive tool results
3. **Batching**: Batch multiple operations when possible
4. **Lazy Loading**: Load widget data on demand
5. **Compression**: Compress large widget payloads

---

## Testing Tools and Widgets

### Unit Testing Tools

```python
import pytest

@pytest.mark.asyncio
async def test_search_tool():
    result = search_database("test query")
    assert isinstance(result, list)
    assert len(result) > 0
    assert "id" in result[0]

@pytest.mark.asyncio
async def test_async_tool():
    result = await fetch_external_data("https://api.example.com/data")
    assert isinstance(result, dict)
```

### Testing Widgets

```python
@pytest.mark.asyncio
async def test_widget_generation():
    server = MyServer()
    thread = ThreadMetadata(id="test")
    input_msg = UserMessageItem(content="show chart")

    events = []
    async for event in server.respond(thread, input_msg, {}):
        events.append(event)

    # Verify widget was generated
    widget_events = [e for e in events if isinstance(e, WidgetEvent)]
    assert len(widget_events) > 0
    assert widget_events[0].widget_type == "chart"
```

---

## Troubleshooting

### Tools Not Being Called

**Check**:
- Tool docstring is clear and descriptive
- Type hints are correct
- Tool is registered in agent's `tools` list
- Agent instructions mention the tool

### Widget Not Rendering

**Check**:
- Widget type is supported by frontend
- Data structure matches expected format
- Widget event is being yielded correctly
- Frontend has widget renderer registered

### Attachment Upload Failing

**Check**:
- `AttachmentStore` is configured
- File size is within limits
- Content type is supported
- Storage backend is accessible
