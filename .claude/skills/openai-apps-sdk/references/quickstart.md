# Quickstart Examples

Complete working examples from hello world to production ChatGPT Apps.

---

## Example 1: Hello World (5 minutes)

Simplest MCP server with text-only response.

### Setup

```bash
mkdir chatgpt-hello-world
cd chatgpt-hello-world
npm init -y
npm install @openai/apps-sdk
```

### Implementation

**server.js**:
```javascript
const { McpServer, StreamableHTTPServerTransport } = require("@openai/apps-sdk");
const { createServer } = require("http");

// Create MCP server
const mcpServer = new McpServer({
  name: "hello-world",
  version: "1.0.0"
});

// Register greeting tool
mcpServer.registerTool(
  "greet",
  {
    title: "Greet User",
    description: "Returns a friendly greeting",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "User's name" }
      },
      required: ["name"]
    }
  },
  async (args) => {
    return {
      content: [{ type: "text", text: `Hello, ${args.name}! Welcome to ChatGPT Apps!` }]
    };
  }
);

// Create HTTP server
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
    await mcpServer.connect(transport);
    await transport.handleRequest(req, res);
    return;
  }

  res.writeHead(200).end("Hello World MCP Server");
});

httpServer.listen(8787, () => {
  console.log("Server running on http://localhost:8787/mcp");
});
```

### Run

```bash
node server.js
```

### Test in ChatGPT

1. Add MCP server: `http://localhost:8787/mcp`
2. Say: "Greet me as Alice"
3. ChatGPT calls the tool and shows: "Hello, Alice! Welcome to ChatGPT Apps!"

---

## Example 2: Simple Widget (15 minutes)

MCP server that returns a widget.

### Setup

```bash
mkdir chatgpt-widget-demo
cd chatgpt-widget-demo
npm init -y
npm install @openai/apps-sdk
```

### Implementation

**widget.html**:
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: system-ui, -apple-system, sans-serif;
      padding: 16px;
      margin: 0;
      background: white;
    }
    [data-theme="dark"] body {
      background: #1a1a1a;
      color: white;
    }
    .card {
      background: #f5f5f5;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    [data-theme="dark"] .card {
      background: #2a2a2a;
    }
    .title {
      font-size: 24px;
      font-weight: 600;
      margin-bottom: 8px;
      color: #0066cc;
    }
    .message {
      font-size: 16px;
      line-height: 1.5;
      color: #333;
    }
    [data-theme="dark"] .message {
      color: #ddd;
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    // Apply theme
    const theme = window.openai?.theme || 'light';
    document.documentElement.setAttribute('data-theme', theme);

    // Read tool output
    const data = window.openai?.toolOutput || {};

    // Render
    document.getElementById('app').innerHTML = `
      <div class="card">
        <div class="title">${data.title || 'Hello!'}</div>
        <div class="message">${data.message || 'Welcome to ChatGPT Apps'}</div>
      </div>
    `;
  </script>
</body>
</html>
```

**server.js**:
```javascript
const { readFileSync } = require("fs");
const { createServer } = require("http");
const { McpServer, StreamableHTTPServerTransport } = require("@openai/apps-sdk");

const widgetHtml = readFileSync("widget.html", "utf8");

const mcpServer = new McpServer({ name: "widget-demo", version: "1.0.0" });

// Register widget resource
mcpServer.registerResource(
  "greeting-widget",
  "ui://widget/greeting.html",
  {},
  async () => ({
    contents: [{
      uri: "ui://widget/greeting.html",
      mimeType: "text/html+skybridge",
      text: widgetHtml,
      _meta: { "openai/widgetPrefersBorder": true }
    }]
  })
);

// Register tool that returns widget
mcpServer.registerTool(
  "show_greeting",
  {
    title: "Show Greeting",
    description: "Displays a greeting in a widget",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string" }
      },
      required: ["name"]
    },
    _meta: {
      "openai/outputTemplate": "ui://widget/greeting.html",
      "openai/toolInvocation/invoking": "Creating greeting...",
      "openai/toolInvocation/invoked": "Greeting ready"
    }
  },
  async (args) => ({
    content: [{ type: "text", text: "Here's your personalized greeting!" }],
    structuredContent: {
      title: `Hello, ${args.name}!`,
      message: `Welcome to ChatGPT Apps. This is your first interactive widget!`
    }
  })
);

// HTTP server
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
    await mcpServer.connect(transport);
    await transport.handleRequest(req, res);
    return;
  }

  res.writeHead(200).end("Widget Demo MCP Server");
});

httpServer.listen(8787, () => {
  console.log("Server running on http://localhost:8787/mcp");
});
```

### Run

```bash
node server.js
```

### Test

In ChatGPT: "Show me a greeting for Bob"

---

## Example 3: Interactive Todo List (30 minutes)

Full todo list with add, complete, and delete functionality.

### Setup

```bash
mkdir chatgpt-todo-app
cd chatgpt-todo-app
npm init -y
npm install @openai/apps-sdk
```

### Implementation

**todo-widget.html**:
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: system-ui;
      padding: 16px;
      margin: 0;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }
    .title {
      font-size: 20px;
      font-weight: 600;
    }
    .count {
      color: #666;
      font-size: 14px;
    }
    .todo-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border-bottom: 1px solid #eee;
      transition: background 0.2s;
    }
    .todo-item:hover {
      background: #f5f5f5;
    }
    .todo-item.completed {
      opacity: 0.6;
    }
    .todo-item.completed .todo-title {
      text-decoration: line-through;
    }
    .checkbox {
      width: 20px;
      height: 20px;
      cursor: pointer;
    }
    .todo-title {
      flex: 1;
      font-size: 16px;
    }
    .delete-btn {
      background: #ff4444;
      color: white;
      border: none;
      padding: 6px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 12px;
    }
    .delete-btn:hover {
      background: #cc0000;
    }
    .empty {
      text-align: center;
      padding: 32px;
      color: #999;
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    const todos = window.openai?.toolOutput?.todos || [];

    function render() {
      const completed = todos.filter(t => t.completed).length;
      const total = todos.length;

      if (total === 0) {
        document.getElementById('app').innerHTML = `
          <div class="empty">
            No todos yet. Ask me to add one!
          </div>
        `;
        return;
      }

      const todosHtml = todos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
          <input
            type="checkbox"
            class="checkbox"
            ${todo.completed ? 'checked' : ''}
            onchange="toggleTodo('${todo.id}')"
          >
          <div class="todo-title">${todo.title}</div>
          <button class="delete-btn" onclick="deleteTodo('${todo.id}')">
            Delete
          </button>
        </div>
      `).join('');

      document.getElementById('app').innerHTML = `
        <div class="header">
          <div class="title">My Todos</div>
          <div class="count">${completed} / ${total} completed</div>
        </div>
        ${todosHtml}
      `;
    }

    async function toggleTodo(id) {
      await window.openai.callTool('complete_todo', { id });
    }

    async function deleteTodo(id) {
      await window.openai.callTool('delete_todo', { id });
    }

    render();
  </script>
</body>
</html>
```

**server.js**:
```javascript
const { readFileSync } = require("fs");
const { createServer } = require("http");
const { McpServer, StreamableHTTPServerTransport } = require("@openai/apps-sdk");

const widgetHtml = readFileSync("todo-widget.html", "utf8");

let todos = [];
let nextId = 1;

const mcpServer = new McpServer({ name: "todo-app", version: "1.0.0" });

// Register widget
mcpServer.registerResource(
  "todo-widget",
  "ui://widget/todo.html",
  {},
  async () => ({
    contents: [{
      uri: "ui://widget/todo.html",
      mimeType: "text/html+skybridge",
      text: widgetHtml,
      _meta: { "openai/widgetPrefersBorder": true }
    }]
  })
);

// Helper to return todos
const returnTodos = (message) => ({
  content: [{ type: "text", text: message }],
  structuredContent: { todos }
});

// Add todo
mcpServer.registerTool(
  "add_todo",
  {
    title: "Add Todo",
    description: "Creates a new todo item",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string", description: "Todo title" }
      },
      required: ["title"]
    },
    _meta: {
      "openai/outputTemplate": "ui://widget/todo.html",
      "openai/toolInvocation/invoking": "Adding todo...",
      "openai/toolInvocation/invoked": "Todo added"
    }
  },
  async (args) => {
    const todo = {
      id: `todo-${nextId++}`,
      title: args.title,
      completed: false
    };
    todos.push(todo);
    return returnTodos(`Added "${todo.title}"`);
  }
);

// Complete todo
mcpServer.registerTool(
  "complete_todo",
  {
    title: "Complete Todo",
    description: "Marks a todo as completed",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string" }
      },
      required: ["id"]
    },
    _meta: { "openai/outputTemplate": "ui://widget/todo.html" }
  },
  async (args) => {
    const todo = todos.find(t => t.id === args.id);
    if (todo) {
      todo.completed = !todo.completed;
      return returnTodos(`Toggled "${todo.title}"`);
    }
    return returnTodos("Todo not found");
  }
);

// Delete todo
mcpServer.registerTool(
  "delete_todo",
  {
    title: "Delete Todo",
    description: "Deletes a todo item",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string" }
      },
      required: ["id"]
    },
    _meta: { "openai/outputTemplate": "ui://widget/todo.html" }
  },
  async (args) => {
    const index = todos.findIndex(t => t.id === args.id);
    if (index !== -1) {
      const deleted = todos.splice(index, 1)[0];
      return returnTodos(`Deleted "${deleted.title}"`);
    }
    return returnTodos("Todo not found");
  }
);

// Get todos
mcpServer.registerTool(
  "get_todos",
  {
    title: "Get Todos",
    description: "Shows all todos",
    inputSchema: { type: "object", properties: {} },
    _meta: { "openai/outputTemplate": "ui://widget/todo.html" }
  },
  async () => returnTodos(`You have ${todos.length} todos`)
);

// HTTP server
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
    await mcpServer.connect(transport);
    await transport.handleRequest(req, res);
    return;
  }

  res.writeHead(200).end("Todo App MCP Server");
});

httpServer.listen(8787, () => {
  console.log("Server running on http://localhost:8787/mcp");
});
```

### Run

```bash
node server.js
```

### Test

In ChatGPT:
- "Add a todo: Buy groceries"
- "Add a todo: Walk the dog"
- "Show my todos"
- Click checkboxes to complete
- Click delete buttons to remove

---

## Example 4: React + Apps SDK UI (45 minutes)

Professional todo app with Apps SDK UI components.

### Setup

```bash
mkdir chatgpt-todo-react
cd chatgpt-todo-react
npm init -y
npm install @openai/apps-sdk react react-dom @openai/apps-sdk-ui
npm install -D vite @vitejs/plugin-react tailwindcss
```

### Configuration

**vite.config.js**:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        entryFileNames: 'widget.js',
        assetFileNames: 'widget.css'
      }
    }
  }
})
```

**tailwind.config.js**:
```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx}",
    "./node_modules/@openai/apps-sdk-ui/**/*.{js,jsx}"
  ],
  theme: { extend: {} },
  plugins: []
}
```

**src/main.css**:
```css
@import "tailwindcss";
@import "@openai/apps-sdk-ui/css";
@source "../node_modules/@openai/apps-sdk-ui";
```

### Widget Implementation

**src/TodoWidget.jsx**:
```jsx
import { useState } from 'react'
import { Button } from '@openai/apps-sdk-ui/components/Button'
import { Badge } from '@openai/apps-sdk-ui/components/Badge'
import { Checkbox } from '@openai/apps-sdk-ui/components/Checkbox'
import { Trash, Plus } from '@openai/apps-sdk-ui/components/Icon'

export function TodoWidget() {
  const todos = window.openai?.toolOutput?.todos || []
  const [loading, setLoading] = useState(null)

  const handleToggle = async (id) => {
    setLoading(id)
    try {
      await window.openai.callTool('complete_todo', { id })
    } finally {
      setLoading(null)
    }
  }

  const handleDelete = async (id) => {
    setLoading(id)
    try {
      await window.openai.callTool('delete_todo', { id })
    } finally {
      setLoading(null)
    }
  }

  const completed = todos.filter(t => t.completed).length

  if (todos.length === 0) {
    return (
      <div className="p-6 text-center text-secondary">
        <p>No todos yet. Ask me to add one!</p>
      </div>
    )
  }

  return (
    <div className="p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="heading-lg">My Todos</h2>
        <Badge color="primary">
          {completed} / {todos.length} done
        </Badge>
      </div>

      <div className="space-y-2">
        {todos.map(todo => (
          <div
            key={todo.id}
            className="flex items-center gap-3 p-3 rounded-lg border border-default hover:bg-surface transition"
          >
            <Checkbox
              checked={todo.completed}
              onChange={() => handleToggle(todo.id)}
              disabled={loading === todo.id}
            />
            <span
              className={`flex-1 ${
                todo.completed ? 'line-through text-secondary' : ''
              }`}
            >
              {todo.title}
            </span>
            <Button
              variant="ghost"
              color="danger"
              size="sm"
              onClick={() => handleDelete(todo.id)}
              disabled={loading === todo.id}
            >
              <Trash />
            </Button>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**src/main.jsx**:
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { TodoWidget } from './TodoWidget'
import './main.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <TodoWidget />
  </React.StrictMode>
)
```

**index.html**:
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

### Build

```bash
npx vite build
```

### Server

Use the same server.js from Example 3, but update widget HTML:

```javascript
const widgetHtml = `
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="http://localhost:5173/widget.css">
</head>
<body>
  <div id="root"></div>
  <script type="module" src="http://localhost:5173/widget.js"></script>
</body>
</html>
`;
```

For production, serve built files from dist/.

---

## Example 5: Production App with Auth (60 minutes)

Complete production app with OAuth authentication.

### Setup

```bash
mkdir chatgpt-production-app
cd chatgpt-production-app
npm init -y
npm install @openai/apps-sdk express dotenv jsonwebtoken
```

### Environment

**.env**:
```
PORT=8787
JWT_SECRET=your-secret-key
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
```

### Implementation

**server.js**:
```javascript
require('dotenv').config()
const express = require('express')
const jwt = require('jsonwebtoken')
const { McpServer, StreamableHTTPServerTransport } = require('@openai/apps-sdk')

const app = express()
const mcpServer = new McpServer({ name: 'production-app', version: '1.0.0' })

// Mock user database
const users = new Map()

// Verify JWT token
function verifyToken(token) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET)
  } catch {
    return null
  }
}

// Register protected tool
mcpServer.registerTool(
  'get_user_data',
  {
    title: 'Get User Data',
    description: 'Retrieves user-specific data',
    inputSchema: { type: 'object', properties: {} },
    securitySchemes: [
      { type: 'oauth2', scopes: ['user.read'] }
    ]
  },
  async (args, context) => {
    // Check for token
    const authHeader = context.headers?.authorization
    if (!authHeader?.startsWith('Bearer ')) {
      return {
        content: [{ type: 'text', text: 'Authentication required' }],
        _meta: {
          'mcp/www_authenticate': [
            `Bearer resource_metadata="http://localhost:${process.env.PORT}/.well-known/oauth-protected-resource", error="insufficient_scope", error_description="Please login to continue"`
          ]
        },
        isError: true
      }
    }

    // Verify token
    const token = authHeader.substring(7)
    const decoded = verifyToken(token)

    if (!decoded) {
      return {
        content: [{ type: 'text', text: 'Invalid token' }],
        isError: true
      }
    }

    // Get user data
    const userData = users.get(decoded.userId) || {
      userId: decoded.userId,
      name: 'Demo User',
      email: 'demo@example.com'
    }

    return {
      content: [{ type: 'text', text: 'Retrieved user data' }],
      structuredContent: { user: userData }
    }
  }
)

// OAuth metadata endpoint
app.get('/.well-known/oauth-protected-resource', (req, res) => {
  res.json({
    resource: `http://localhost:${process.env.PORT}`,
    authorization_servers: [`http://localhost:${process.env.PORT}/oauth`],
    bearer_methods_supported: ['header'],
    resource_documentation: 'https://docs.example.com'
  })
})

// CORS middleware
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
  res.header('Access-Control-Allow-Headers', 'content-type, mcp-session-id, authorization')
  res.header('Access-Control-Expose-Headers', 'Mcp-Session-Id')
  if (req.method === 'OPTIONS') {
    return res.sendStatus(204)
  }
  next()
})

// MCP endpoint
app.post('/mcp', async (req, res) => {
  const transport = new StreamableHTTPServerTransport()
  await mcpServer.connect(transport)
  await transport.handleRequest(req, res)
})

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', version: '1.0.0' })
})

// Start server
const PORT = process.env.PORT || 8787
app.listen(PORT, () => {
  console.log(`Production server running on http://localhost:${PORT}/mcp`)
})
```

### Run

```bash
node server.js
```

---

## Deployment Patterns

### Docker

**Dockerfile**:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY . .

EXPOSE 8787

CMD ["node", "server.js"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8787:8787"
    environment:
      - NODE_ENV=production
      - PORT=8787
    restart: unless-stopped
```

Build and run:
```bash
docker-compose up -d
```

---

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

---

### Render

**render.yaml**:
```yaml
services:
  - type: web
    name: chatgpt-app
    env: node
    buildCommand: npm install
    startCommand: node server.js
    envVars:
      - key: NODE_ENV
        value: production
```

---

## Testing

### Unit Tests

**server.test.js**:
```javascript
const { describe, it, expect } = require('@jest/globals')

describe('Todo Tools', () => {
  it('should add todo', async () => {
    const result = await addTodoTool({ title: 'Test' })
    expect(result.structuredContent.todos).toHaveLength(1)
    expect(result.structuredContent.todos[0].title).toBe('Test')
  })

  it('should complete todo', async () => {
    await addTodoTool({ title: 'Test' })
    const result = await completeTodoTool({ id: 'todo-1' })
    expect(result.structuredContent.todos[0].completed).toBe(true)
  })
})
```

---

## Troubleshooting

### Server Not Starting

```bash
# Check port availability
lsof -i :8787

# Check Node version
node --version  # Should be 16+

# Check dependencies
npm list
```

### Widget Not Rendering

**Check**:
- Widget HTML is valid
- `_meta["openai/outputTemplate"]` matches resource URI
- CORS headers are set correctly
- Browser console for errors

### Tool Not Appearing

**Check**:
- Tool is registered before server starts
- Input schema is valid JSON Schema
- MCP server is running
- ChatGPT can reach the server

### State Not Persisting

**Check**:
- `window.openai.setWidgetState()` is called
- State object is serializable (no functions)
- State is under 4k tokens

---

## Next Steps

1. **Explore Examples**: Try all examples in order
2. **Customize**: Modify widgets and tools for your use case
3. **Add Features**: Implement search, filters, pagination
4. **Add Auth**: Implement OAuth for user-specific data
5. **Deploy**: Deploy to production with Docker/Railway/Render
6. **Monitor**: Add logging and error tracking
7. **Iterate**: Improve based on user feedback

See other reference files for detailed patterns and best practices.
