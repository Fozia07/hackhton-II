---
name: openai-apps-sdk
description: Builds interactive ChatGPT Apps with widgets using OpenAI Apps SDK and Model Context Protocol (MCP). This skill should be used when users want to create ChatGPT Apps, build custom widgets for ChatGPT, implement MCP servers with tools, integrate Apps SDK UI components, add OAuth authentication, or develop production-ready interactive applications that render inside ChatGPT conversations. Handles MCP server setup, widget development, state management, and deployment patterns.
---

# OpenAI Apps SDK

Build interactive ChatGPT Apps with custom widgets from hello world to production systems.

## What This Skill Does

- Creates MCP (Model Context Protocol) servers that expose tools to ChatGPT
- Builds custom widgets (HTML/CSS/JS) that render inside ChatGPT
- Implements React components using Apps SDK UI design system
- Sets up state management with `window.openai` API
- Configures OAuth authentication flows
- Provides production deployment patterns

## What This Skill Does NOT Do

- Build standalone web applications (Apps SDK is for ChatGPT integration)
- Handle non-ChatGPT AI platforms
- Manage infrastructure provisioning
- Deploy to specific cloud providers (provides patterns only)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing MCP servers, widget code, project structure |
| **Conversation** | User's requirements: app type, features, authentication needs |
| **Skill References** | Apps SDK patterns from `references/` (MCP, widgets, UI components) |
| **User Guidelines** | Team conventions, security requirements, tech stack |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Core Architecture

### How Apps SDK Works

```
User talks to ChatGPT
       ↓
ChatGPT calls MCP tool
       ↓
MCP server returns:
  - Structured content (data)
  - Widget metadata (_meta)
       ↓
ChatGPT renders widget inline
       ↓
Widget uses window.openai API
  - Read tool output
  - Call tools
  - Manage state
  - Send follow-ups
```

### Key Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **MCP Server** | Exposes tools to ChatGPT | Node.js or Python |
| **Tools** | Functions ChatGPT can call | JSON Schema + handlers |
| **Widgets** | UI rendered in ChatGPT | HTML/CSS/JS (React optional) |
| **Apps SDK UI** | Pre-built components | React + Tailwind CSS |
| **window.openai** | Bridge between widget and ChatGPT | JavaScript API |

---

## Implementation Levels

Progressive complexity for different use cases:

| Level | Capability | When to Use |
|-------|-----------|-------------|
| **Hello World** | Simple tool + text response | Learning, prototyping |
| **Basic Widget** | Tool returns HTML widget | Interactive displays |
| **Stateful Widget** | Widget manages state | Multi-step interactions |
| **Apps SDK UI** | Professional React components | Production apps |
| **Authenticated** | OAuth-protected tools | User-specific data |
| **Production** | Full error handling, monitoring | Real applications |

---

## Core Workflow

### 1. Clarify Requirements

Ask user about THEIR specific needs:

| Question | Purpose |
|----------|---------|
| **App type** | What does the app do? (todo list, search, booking, etc.) |
| **Interactivity** | Static display or interactive widget? |
| **State** | Does widget need to remember data across interactions? |
| **Authentication** | Public or user-specific data? |
| **UI framework** | Vanilla JS, React, or Apps SDK UI components? |
| **Backend** | Node.js or Python for MCP server? |

### 2. Choose Architecture Pattern

Based on requirements, select from `references/mcp-servers.md`:

- **Simple Tool**: Text-only response (no widget)
- **Static Widget**: Display-only HTML
- **Interactive Widget**: Buttons, forms, state management
- **Authenticated App**: OAuth-protected tools
- **Production App**: Full error handling, monitoring

### 3. Set Up MCP Server

Create MCP server that exposes tools:

**Node.js**:
```javascript
const { McpServer } = require("@openai/apps-sdk");

const server = new McpServer({ name: "my-app", version: "1.0.0" });

server.registerTool(
  "my_tool",
  {
    title: "My Tool",
    description: "Does something useful",
    inputSchema: { /* JSON Schema */ },
    _meta: {
      "openai/outputTemplate": "ui://widget/my-widget.html"
    }
  },
  async (args) => {
    return {
      content: [{ type: "text", text: "Success!" }],
      structuredContent: { /* data for widget */ }
    };
  }
);
```

**Python**:
```python
from mcp.server import Server

server = Server("my-app")

@server.tool("my_tool")
async def my_tool(args):
    return {
        "content": [{"type": "text", "text": "Success!"}],
        "structuredContent": { /* data */ }
    }
```

### 4. Create Widget

Build HTML/CSS/JS widget that renders in ChatGPT:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Widget styles */
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    // Access tool output
    const data = window.openai.toolOutput;

    // Render UI
    document.getElementById('app').innerHTML = `
      <h1>${data.title}</h1>
      <button onclick="handleClick()">Action</button>
    `;

    // Handle interactions
    async function handleClick() {
      await window.openai.callTool("my_tool", { action: "click" });
    }
  </script>
</body>
</html>
```

### 5. Register Widget Resource

Tell MCP server about the widget:

```javascript
server.registerResource(
  "my-widget",
  "ui://widget/my-widget.html",
  {},
  async () => ({
    contents: [{
      uri: "ui://widget/my-widget.html",
      mimeType: "text/html+skybridge",
      text: widgetHtml,
      _meta: { "openai/widgetPrefersBorder": true }
    }]
  })
);
```

### 6. Add State Management (Optional)

For stateful widgets:

```javascript
// In widget
window.openai.setWidgetState({ selectedId: "123" });

// Read state
const state = window.openai.widgetState || {};
```

### 7. Add Authentication (Optional)

For user-specific data:

```javascript
server.registerTool(
  "protected_tool",
  {
    title: "Protected Tool",
    description: "Requires authentication",
    inputSchema: { /* schema */ },
    securitySchemes: [
      { type: "oauth2", scopes: ["read", "write"] }
    ]
  },
  async (args, context) => {
    // Verify token
    if (!context.token) {
      return {
        content: [{ type: "text", text: "Authentication required" }],
        _meta: {
          "mcp/www_authenticate": [
            'Bearer resource_metadata="https://your-server.com/.well-known/oauth-protected-resource"'
          ]
        },
        isError: true
      };
    }

    // Process authenticated request
    return { /* response */ };
  }
);
```

### 8. Test and Deploy

- Test locally with ChatGPT
- Add error handling and logging
- Deploy MCP server to production
- Configure ChatGPT to use your MCP server

---

## Quick Start Examples

### Hello World (Text Only)

Simplest MCP server with no widget:

```javascript
const { McpServer } = require("@openai/apps-sdk");

const server = new McpServer({ name: "hello", version: "1.0.0" });

server.registerTool(
  "greet",
  {
    title: "Greet User",
    description: "Says hello",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string" }
      }
    }
  },
  async (args) => ({
    content: [{ type: "text", text: `Hello, ${args.name}!` }]
  })
);
```

### Simple Widget

Tool that returns a widget:

```javascript
const widgetHtml = `
<!DOCTYPE html>
<html>
<body>
  <div id="app"></div>
  <script>
    const data = window.openai.toolOutput;
    document.getElementById('app').innerHTML =
      '<h1>' + data.message + '</h1>';
  </script>
</body>
</html>
`;

server.registerResource("greeting-widget", "ui://widget/greeting.html", {},
  async () => ({
    contents: [{
      uri: "ui://widget/greeting.html",
      mimeType: "text/html+skybridge",
      text: widgetHtml
    }]
  })
);

server.registerTool(
  "greet_with_widget",
  {
    title: "Greet with Widget",
    description: "Shows greeting in widget",
    inputSchema: { type: "object", properties: { name: { type: "string" } } },
    _meta: { "openai/outputTemplate": "ui://widget/greeting.html" }
  },
  async (args) => ({
    content: [{ type: "text", text: "Showing greeting" }],
    structuredContent: { message: `Hello, ${args.name}!` }
  })
);
```

See `references/quickstart.md` for complete examples.

---

## Key Concepts

### Model Context Protocol (MCP)

Open standard for connecting AI models to tools and data:

- **Tools**: Functions the model can call
- **Resources**: Static content (like widget HTML)
- **Prompts**: Reusable prompt templates
- **Transport**: HTTP or SSE for communication

### Tools

Functions exposed to ChatGPT:

- **Input Schema**: JSON Schema defining parameters
- **Handler**: Async function that executes the tool
- **Output**: Text content + structured data
- **Metadata**: Widget templates, auth requirements

### Widgets

HTML/CSS/JS components rendered in ChatGPT:

- **Inline Rendering**: Appears in conversation
- **window.openai API**: Access to ChatGPT features
- **State Management**: Persist data across interactions
- **Responsive**: Works on mobile, tablet, desktop

### window.openai API

JavaScript API available in widgets:

```javascript
// Read data
window.openai.toolOutput      // Tool's structured content
window.openai.widgetState     // Persisted state
window.openai.locale          // User's locale
window.openai.theme           // "light" or "dark"

// Actions
window.openai.callTool(name, args)           // Call another tool
window.openai.setWidgetState(state)          // Persist state
window.openai.sendFollowUpMessage(prompt)    // Send message
window.openai.openExternal({ href: url })    // Open link
window.openai.requestDisplayMode({ mode })   // Request fullscreen
```

### Apps SDK UI

Pre-built React components with Tailwind CSS:

- **Components**: Button, Badge, Card, Input, etc.
- **Icons**: 100+ icons
- **Design Tokens**: Colors, spacing, typography
- **Responsive**: Mobile-first design
- **Accessible**: WCAG compliant

---

## Common Patterns

### Pattern: Interactive Todo List

```javascript
// MCP Server
let todos = [];

server.registerTool("add_todo", {
  title: "Add Todo",
  inputSchema: { type: "object", properties: { title: { type: "string" } } },
  _meta: { "openai/outputTemplate": "ui://widget/todos.html" }
}, async (args) => {
  todos.push({ id: Date.now(), title: args.title, done: false });
  return {
    content: [{ type: "text", text: "Added todo" }],
    structuredContent: { todos }
  };
});

// Widget
const widgetHtml = `
<div id="app"></div>
<script>
  const todos = window.openai.toolOutput.todos || [];

  function render() {
    document.getElementById('app').innerHTML = todos.map(todo =>
      '<div>' + todo.title + '</div>'
    ).join('');
  }

  render();
</script>
`;
```

### Pattern: Stateful Widget

```javascript
// Widget with state
const state = window.openai.widgetState || { selectedId: null };

function selectItem(id) {
  window.openai.setWidgetState({ selectedId: id });
  render();
}
```

### Pattern: OAuth Authentication

```javascript
server.registerTool("get_user_data", {
  title: "Get User Data",
  securitySchemes: [{ type: "oauth2", scopes: ["user.read"] }]
}, async (args, context) => {
  if (!context.token) {
    return {
      content: [{ type: "text", text: "Please authenticate" }],
      _meta: { "mcp/www_authenticate": [...] },
      isError: true
    };
  }

  // Fetch user data with token
  const userData = await fetchUserData(context.token);
  return { structuredContent: userData };
});
```

See `references/mcp-servers.md` for complete patterns.

---

## Dependencies

### MCP Server (Node.js)

```bash
npm install @openai/apps-sdk @modelcontextprotocol/sdk zod
```

### MCP Server (Python)

```bash
pip install mcp openai-apps-sdk
```

### Widget (React + Apps SDK UI)

```bash
npm install react react-dom @openai/apps-sdk-ui
npm install -D tailwindcss
```

---

## Production Checklist

Before deploying to production:

- [ ] Add comprehensive error handling in tools
- [ ] Implement request validation with JSON Schema
- [ ] Add logging and monitoring
- [ ] Configure CORS for ChatGPT domains
- [ ] Set up OAuth if using authentication
- [ ] Test widgets on mobile, tablet, desktop
- [ ] Test light and dark themes
- [ ] Optimize widget bundle size
- [ ] Add rate limiting to prevent abuse
- [ ] Document tool usage for users
- [ ] Set up CI/CD pipeline
- [ ] Configure production environment variables

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Widget not rendering** | Check `_meta["openai/outputTemplate"]` matches resource URI |
| **window.openai undefined** | Widget not loaded in ChatGPT context |
| **Tool not appearing** | Verify tool registration and MCP server is running |
| **State not persisting** | Ensure `setWidgetState` is called correctly |
| **OAuth not working** | Check security schemes and WWW-Authenticate headers |
| **CORS errors** | Add ChatGPT domains to CORS allowlist |

### Debug Mode

Enable detailed logging:

```javascript
// Node.js
console.log("Tool called:", args);
console.log("Context:", context);

// Widget
console.log("Tool output:", window.openai.toolOutput);
console.log("Widget state:", window.openai.widgetState);
```

---

## Reference Files

| File | Content |
|------|---------|
| `references/mcp-servers.md` | MCP server patterns, tools, authentication |
| `references/widgets.md` | Widget development, window.openai API, state management |
| `references/ui-components.md` | Apps SDK UI components, React patterns, Tailwind |
| `references/quickstart.md` | Complete working examples from hello world to production |

---

## Example: Complete Todo App

**MCP Server (server.js)**:
```javascript
const { readFileSync } = require("fs");
const { createServer } = require("http");
const { McpServer, StreamableHTTPServerTransport } = require("@openai/apps-sdk");

const widgetHtml = readFileSync("widget.html", "utf8");
let todos = [];
let nextId = 1;

const server = new McpServer({ name: "todo-app", version: "1.0.0" });

server.registerResource("todo-widget", "ui://widget/todo.html", {},
  async () => ({
    contents: [{
      uri: "ui://widget/todo.html",
      mimeType: "text/html+skybridge",
      text: widgetHtml,
      _meta: { "openai/widgetPrefersBorder": true }
    }]
  })
);

server.registerTool("add_todo", {
  title: "Add Todo",
  description: "Creates a todo item",
  inputSchema: {
    type: "object",
    properties: { title: { type: "string" } },
    required: ["title"]
  },
  _meta: {
    "openai/outputTemplate": "ui://widget/todo.html",
    "openai/toolInvocation/invoking": "Adding todo",
    "openai/toolInvocation/invoked": "Added todo"
  }
}, async (args) => {
  const todo = { id: `todo-${nextId++}`, title: args.title, completed: false };
  todos.push(todo);
  return {
    content: [{ type: "text", text: `Added "${todo.title}"` }],
    structuredContent: { todos }
  };
});

server.registerTool("complete_todo", {
  title: "Complete Todo",
  description: "Marks a todo as done",
  inputSchema: {
    type: "object",
    properties: { id: { type: "string" } },
    required: ["id"]
  },
  _meta: { "openai/outputTemplate": "ui://widget/todo.html" }
}, async (args) => {
  const todo = todos.find(t => t.id === args.id);
  if (todo) {
    todo.completed = true;
    return {
      content: [{ type: "text", text: `Completed "${todo.title}"` }],
      structuredContent: { todos }
    };
  }
  return {
    content: [{ type: "text", text: "Todo not found" }],
    structuredContent: { todos }
  };
});

// HTTP server setup
const httpServer = createServer(async (req, res) => {
  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      "Access-Control-Allow-Headers": "content-type, mcp-session-id"
    });
    res.end();
    return;
  }

  if (req.url === "/mcp" && req.method === "POST") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    const transport = new StreamableHTTPServerTransport();
    await server.connect(transport);
    await transport.handleRequest(req, res);
    return;
  }

  res.writeHead(404).end("Not Found");
});

httpServer.listen(8787, () => {
  console.log("MCP server running on http://localhost:8787/mcp");
});
```

**Widget (widget.html)**:
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: system-ui; padding: 16px; }
    .todo { padding: 8px; border-bottom: 1px solid #eee; }
    .todo.completed { text-decoration: line-through; opacity: 0.6; }
    button { margin-top: 8px; padding: 8px 16px; cursor: pointer; }
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    const todos = window.openai.toolOutput?.todos || [];

    function render() {
      const html = todos.map(todo => `
        <div class="todo ${todo.completed ? 'completed' : ''}">
          ${todo.title}
          ${!todo.completed ? `
            <button onclick="completeTodo('${todo.id}')">Complete</button>
          ` : ''}
        </div>
      `).join('');

      document.getElementById('app').innerHTML = html || '<p>No todos yet</p>';
    }

    async function completeTodo(id) {
      await window.openai.callTool("complete_todo", { id });
    }

    render();
  </script>
</body>
</html>
```

Run with:
```bash
node server.js
```

Then in ChatGPT, add the MCP server and say: "Add a todo: Buy groceries"

---

## Next Steps

After implementing basic app:

1. **Add More Tools**: Expand functionality with additional tools
2. **Improve UI**: Use Apps SDK UI components for professional look
3. **Add Authentication**: Implement OAuth for user-specific data
4. **State Management**: Add complex state handling
5. **Error Handling**: Implement comprehensive error handling
6. **Deploy**: Follow production deployment patterns
7. **Monitor**: Add logging and analytics
8. **Iterate**: Improve based on user feedback

See reference files for detailed guidance on each step.
