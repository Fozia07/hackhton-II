# MCP Server Patterns

Comprehensive guide to building Model Context Protocol (MCP) servers for OpenAI Apps SDK.

---

## MCP Server Fundamentals

### What is MCP?

Model Context Protocol is an open standard for connecting AI models to:
- **Tools**: Functions the model can call
- **Resources**: Static content (HTML, data)
- **Prompts**: Reusable prompt templates

### MCP Server Architecture

```
ChatGPT
    ↓ (calls tool)
MCP Server
    ↓ (executes)
Tool Handler
    ↓ (returns)
{
  content: [...],           // Text for ChatGPT
  structuredContent: {...}, // Data for widget
  _meta: {...}             // Widget metadata
}
```

---

## Server Setup Patterns

### Pattern 1: Basic Node.js Server

```javascript
const { McpServer, StreamableHTTPServerTransport } = require("@openai/apps-sdk");
const { createServer } = require("http");

// Create MCP server
const mcpServer = new McpServer({
  name: "my-app",
  version: "1.0.0"
});

// Register tools (see Tool Patterns below)
mcpServer.registerTool("my_tool", { /* config */ }, async (args) => {
  return { content: [{ type: "text", text: "Result" }] };
});

// Create HTTP server
const httpServer = createServer(async (req, res) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      "Access-Control-Allow-Headers": "content-type, mcp-session-id",
      "Access-Control-Expose-Headers": "Mcp-Session-Id"
    });
    res.end();
    return;
  }

  // Handle MCP requests
  if (req.url === "/mcp" && req.method === "POST") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");

    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined, // stateless mode
      enableJsonResponse: true
    });

    res.on("close", () => {
      transport.close();
      mcpServer.close();
    });

    try {
      await mcpServer.connect(transport);
      await transport.handleRequest(req, res);
    } catch (error) {
      console.error("MCP error:", error);
      if (!res.headersSent) {
        res.writeHead(500).end("Internal server error");
      }
    }
    return;
  }

  res.writeHead(404).end("Not Found");
});

httpServer.listen(8787, () => {
  console.log("MCP server running on http://localhost:8787/mcp");
});
```

---

### Pattern 2: Python MCP Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

# Create server
server = Server("my-app")

# Register tool
@server.tool("my_tool")
async def my_tool(args: dict) -> dict:
    """Tool description for ChatGPT"""
    return {
        "content": [{"type": "text", "text": "Result"}],
        "structuredContent": {"data": "value"}
    }

# Run server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

---

### Pattern 3: Express.js Integration

```javascript
const express = require("express");
const { McpServer, StreamableHTTPServerTransport } = require("@openai/apps-sdk");

const app = express();
const mcpServer = new McpServer({ name: "my-app", version: "1.0.0" });

// Register tools
mcpServer.registerTool("my_tool", { /* config */ }, async (args) => {
  return { content: [{ type: "text", text: "Result" }] };
});

// CORS middleware
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  res.header("Access-Control-Allow-Headers", "content-type, mcp-session-id");
  res.header("Access-Control-Expose-Headers", "Mcp-Session-Id");
  if (req.method === "OPTIONS") {
    return res.sendStatus(204);
  }
  next();
});

// MCP endpoint
app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport();
  await mcpServer.connect(transport);
  await transport.handleRequest(req, res);
});

app.listen(8787, () => {
  console.log("Server running on http://localhost:8787");
});
```

---

## Tool Registration Patterns

### Pattern 1: Simple Tool (Text Only)

```javascript
mcpServer.registerTool(
  "greet",
  {
    title: "Greet User",
    description: "Returns a greeting message",
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
      content: [{ type: "text", text: `Hello, ${args.name}!` }]
    };
  }
);
```

---

### Pattern 2: Tool with Widget

```javascript
mcpServer.registerTool(
  "show_data",
  {
    title: "Show Data",
    description: "Displays data in a widget",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string" }
      }
    },
    _meta: {
      "openai/outputTemplate": "ui://widget/data-display.html",
      "openai/toolInvocation/invoking": "Fetching data...",
      "openai/toolInvocation/invoked": "Data ready",
      "openai/widgetAccessible": true,
      "openai/resultCanProduceWidget": true
    }
  },
  async (args) => {
    const data = await fetchData(args.query);

    return {
      content: [{ type: "text", text: "Here's your data" }],
      structuredContent: {
        items: data.items,
        total: data.total
      },
      _meta: {
        "openai/outputTemplate": "ui://widget/data-display.html",
        "openai/widgetAccessible": true,
        "openai/resultCanProduceWidget": true
      }
    };
  }
);
```

---

### Pattern 3: Tool with Complex Schema

```javascript
mcpServer.registerTool(
  "search_products",
  {
    title: "Search Products",
    description: "Search product catalog with filters",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Search query"
        },
        category: {
          type: "string",
          enum: ["electronics", "clothing", "books", "home"],
          description: "Product category"
        },
        priceRange: {
          type: "object",
          properties: {
            min: { type: "number", minimum: 0 },
            max: { type: "number", minimum: 0 }
          }
        },
        sortBy: {
          type: "string",
          enum: ["relevance", "price_low", "price_high", "rating"],
          default: "relevance"
        },
        limit: {
          type: "integer",
          minimum: 1,
          maximum: 100,
          default: 10
        }
      },
      required: ["query"]
    }
  },
  async (args) => {
    const results = await searchProducts({
      query: args.query,
      category: args.category,
      priceRange: args.priceRange,
      sortBy: args.sortBy || "relevance",
      limit: args.limit || 10
    });

    return {
      content: [{ type: "text", text: `Found ${results.length} products` }],
      structuredContent: { products: results }
    };
  }
);
```

---

### Pattern 4: Tool with Validation

```javascript
const { z } = require("zod");

// Define schema with Zod
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(18).max(120).optional()
});

mcpServer.registerTool(
  "create_user",
  {
    title: "Create User",
    description: "Creates a new user account",
    inputSchema: {
      type: "object",
      properties: {
        email: { type: "string", format: "email" },
        name: { type: "string", minLength: 1, maxLength: 100 },
        age: { type: "integer", minimum: 18, maximum: 120 }
      },
      required: ["email", "name"]
    }
  },
  async (args) => {
    try {
      // Validate with Zod
      const validated = createUserSchema.parse(args);

      // Create user
      const user = await createUser(validated);

      return {
        content: [{ type: "text", text: `Created user: ${user.name}` }],
        structuredContent: { user }
      };
    } catch (error) {
      if (error instanceof z.ZodError) {
        return {
          content: [{ type: "text", text: `Validation error: ${error.message}` }],
          isError: true
        };
      }
      throw error;
    }
  }
);
```

---

## Resource Registration

### Pattern 1: Static Widget Resource

```javascript
const { readFileSync } = require("fs");

const widgetHtml = readFileSync("widgets/my-widget.html", "utf8");

mcpServer.registerResource(
  "my-widget",
  "ui://widget/my-widget.html",
  {},
  async () => ({
    contents: [{
      uri: "ui://widget/my-widget.html",
      mimeType: "text/html+skybridge",
      text: widgetHtml,
      _meta: {
        "openai/widgetPrefersBorder": true,
        "openai/widgetMinHeight": "200px"
      }
    }]
  })
);
```

---

### Pattern 2: Dynamic Widget Resource

```javascript
mcpServer.registerResource(
  "dynamic-widget",
  "ui://widget/dynamic.html",
  {},
  async (uri, context) => {
    // Generate widget HTML dynamically
    const widgetHtml = generateWidgetHtml(context);

    return {
      contents: [{
        uri: "ui://widget/dynamic.html",
        mimeType: "text/html+skybridge",
        text: widgetHtml
      }]
    };
  }
);
```

---

### Pattern 3: Multiple Resources

```javascript
// Register multiple widget variants
const widgets = {
  "list-view": readFileSync("widgets/list.html", "utf8"),
  "grid-view": readFileSync("widgets/grid.html", "utf8"),
  "detail-view": readFileSync("widgets/detail.html", "utf8")
};

Object.entries(widgets).forEach(([name, html]) => {
  mcpServer.registerResource(
    name,
    `ui://widget/${name}.html`,
    {},
    async () => ({
      contents: [{
        uri: `ui://widget/${name}.html`,
        mimeType: "text/html+skybridge",
        text: html
      }]
    })
  );
});
```

---

## State Management Patterns

### Pattern 1: In-Memory State

```javascript
// Simple in-memory state
const state = {
  todos: [],
  nextId: 1
};

mcpServer.registerTool("add_todo", {
  title: "Add Todo",
  inputSchema: { type: "object", properties: { title: { type: "string" } } }
}, async (args) => {
  const todo = {
    id: `todo-${state.nextId++}`,
    title: args.title,
    completed: false
  };
  state.todos.push(todo);

  return {
    content: [{ type: "text", text: "Added todo" }],
    structuredContent: { todos: state.todos }
  };
});
```

---

### Pattern 2: Database State

```javascript
const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

mcpServer.registerTool("get_tasks", {
  title: "Get Tasks",
  inputSchema: { type: "object", properties: {} }
}, async (args) => {
  const result = await pool.query("SELECT * FROM tasks ORDER BY created_at DESC");

  return {
    content: [{ type: "text", text: `Found ${result.rows.length} tasks` }],
    structuredContent: { tasks: result.rows }
  };
});

mcpServer.registerTool("add_task", {
  title: "Add Task",
  inputSchema: {
    type: "object",
    properties: { title: { type: "string" } },
    required: ["title"]
  }
}, async (args) => {
  const result = await pool.query(
    "INSERT INTO tasks (title, completed) VALUES ($1, $2) RETURNING *",
    [args.title, false]
  );

  const allTasks = await pool.query("SELECT * FROM tasks ORDER BY created_at DESC");

  return {
    content: [{ type: "text", text: "Added task" }],
    structuredContent: { tasks: allTasks.rows }
  };
});
```

---

### Pattern 3: External API State

```javascript
const axios = require("axios");

mcpServer.registerTool("get_user_preferences", {
  title: "Get User Preferences",
  inputSchema: {
    type: "object",
    properties: { userId: { type: "string" } },
    required: ["userId"]
  }
}, async (args) => {
  const response = await axios.get(
    `https://api.example.com/users/${args.userId}/preferences`,
    {
      headers: { Authorization: `Bearer ${process.env.API_TOKEN}` }
    }
  );

  return {
    content: [{ type: "text", text: "Retrieved preferences" }],
    structuredContent: { preferences: response.data }
  };
});

mcpServer.registerTool("update_preferences", {
  title: "Update Preferences",
  inputSchema: {
    type: "object",
    properties: {
      userId: { type: "string" },
      preferences: { type: "object" }
    },
    required: ["userId", "preferences"]
  }
}, async (args) => {
  const response = await axios.put(
    `https://api.example.com/users/${args.userId}/preferences`,
    args.preferences,
    {
      headers: {
        Authorization: `Bearer ${process.env.API_TOKEN}`,
        "Content-Type": "application/json"
      }
    }
  );

  return {
    content: [{ type: "text", text: "Updated preferences" }],
    structuredContent: { preferences: response.data }
  };
});
```

---

## Authentication Patterns

### Pattern 1: Public + Optional Auth

```javascript
mcpServer.registerTool(
  "search",
  {
    title: "Search",
    description: "Search public data (login for personalized results)",
    inputSchema: {
      type: "object",
      properties: { query: { type: "string" } }
    },
    securitySchemes: [
      { type: "noauth" },
      { type: "oauth2", scopes: ["search.read"] }
    ]
  },
  async (args, context) => {
    let results;

    if (context.token) {
      // Authenticated: personalized results
      results = await searchPersonalized(args.query, context.token);
    } else {
      // Anonymous: public results
      results = await searchPublic(args.query);
    }

    return {
      content: [{ type: "text", text: `Found ${results.length} results` }],
      structuredContent: { results }
    };
  }
);
```

---

### Pattern 2: Auth Required

```javascript
mcpServer.registerTool(
  "create_document",
  {
    title: "Create Document",
    description: "Create a new document in your account",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string" },
        content: { type: "string" }
      },
      required: ["title"]
    },
    securitySchemes: [
      { type: "oauth2", scopes: ["docs.write"] }
    ]
  },
  async (args, context) => {
    // Verify token
    if (!context.token) {
      return {
        content: [{ type: "text", text: "Authentication required" }],
        _meta: {
          "mcp/www_authenticate": [
            'Bearer resource_metadata="https://your-server.com/.well-known/oauth-protected-resource", error="insufficient_scope", error_description="You need to login to create documents"'
          ]
        },
        isError: true
      };
    }

    // Verify scopes
    const hasWriteScope = verifyScopes(context.token, ["docs.write"]);
    if (!hasWriteScope) {
      return {
        content: [{ type: "text", text: "Insufficient permissions" }],
        _meta: {
          "mcp/www_authenticate": [
            'Bearer error="insufficient_scope", error_description="You need docs.write permission"'
          ]
        },
        isError: true
      };
    }

    // Create document
    const doc = await createDocument(args, context.token);

    return {
      content: [{ type: "text", text: `Created document: ${doc.title}` }],
      structuredContent: { document: doc }
    };
  }
);
```

---

### Pattern 3: OAuth Configuration

```javascript
// Publish OAuth metadata at /.well-known/oauth-protected-resource
app.get("/.well-known/oauth-protected-resource", (req, res) => {
  res.json({
    resource: "https://your-server.com",
    authorization_servers: ["https://auth.example.com"],
    bearer_methods_supported: ["header"],
    resource_documentation: "https://docs.example.com"
  });
});

// Token verification helper
function verifyToken(token) {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return {
      valid: true,
      userId: decoded.sub,
      scopes: decoded.scope?.split(" ") || []
    };
  } catch (error) {
    return { valid: false };
  }
}

// Scope verification helper
function verifyScopes(token, requiredScopes) {
  const { valid, scopes } = verifyToken(token);
  if (!valid) return false;

  return requiredScopes.every(scope => scopes.includes(scope));
}
```

---

## Error Handling Patterns

### Pattern 1: Graceful Error Responses

```javascript
mcpServer.registerTool("risky_operation", {
  title: "Risky Operation",
  inputSchema: { type: "object", properties: { param: { type: "string" } } }
}, async (args) => {
  try {
    const result = await performRiskyOperation(args.param);
    return {
      content: [{ type: "text", text: "Success!" }],
      structuredContent: { result }
    };
  } catch (error) {
    console.error("Operation failed:", error);

    return {
      content: [{ type: "text", text: `Operation failed: ${error.message}` }],
      isError: true
    };
  }
});
```

---

### Pattern 2: Validation Errors

```javascript
mcpServer.registerTool("create_item", {
  title: "Create Item",
  inputSchema: {
    type: "object",
    properties: {
      name: { type: "string", minLength: 1, maxLength: 100 },
      price: { type: "number", minimum: 0 }
    },
    required: ["name", "price"]
  }
}, async (args) => {
  // Additional validation
  if (args.price > 10000) {
    return {
      content: [{ type: "text", text: "Price too high (max: $10,000)" }],
      isError: true
    };
  }

  if (await itemExists(args.name)) {
    return {
      content: [{ type: "text", text: "Item already exists" }],
      isError: true
    };
  }

  const item = await createItem(args);
  return {
    content: [{ type: "text", text: "Item created" }],
    structuredContent: { item }
  };
});
```

---

### Pattern 3: Retry Logic

```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}

mcpServer.registerTool("fetch_external_data", {
  title: "Fetch External Data",
  inputSchema: { type: "object", properties: { url: { type: "string" } } }
}, async (args) => {
  try {
    const data = await withRetry(() => fetchData(args.url));
    return {
      content: [{ type: "text", text: "Data fetched" }],
      structuredContent: { data }
    };
  } catch (error) {
    return {
      content: [{ type: "text", text: "Failed to fetch data after retries" }],
      isError: true
    };
  }
});
```

---

## Production Patterns

### Pattern 1: Logging and Monitoring

```javascript
const winston = require("winston");

const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" })
  ]
});

mcpServer.registerTool("monitored_tool", {
  title: "Monitored Tool",
  inputSchema: { type: "object", properties: {} }
}, async (args, context) => {
  const startTime = Date.now();

  logger.info("Tool called", {
    tool: "monitored_tool",
    args,
    userId: context.userId
  });

  try {
    const result = await performOperation(args);

    logger.info("Tool succeeded", {
      tool: "monitored_tool",
      duration: Date.now() - startTime
    });

    return {
      content: [{ type: "text", text: "Success" }],
      structuredContent: { result }
    };
  } catch (error) {
    logger.error("Tool failed", {
      tool: "monitored_tool",
      error: error.message,
      stack: error.stack,
      duration: Date.now() - startTime
    });

    return {
      content: [{ type: "text", text: "Operation failed" }],
      isError: true
    };
  }
});
```

---

### Pattern 2: Rate Limiting

```javascript
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests, please try again later"
});

app.use("/mcp", limiter);
```

---

### Pattern 3: Environment Configuration

```javascript
require("dotenv").config();

const config = {
  port: process.env.PORT || 8787,
  databaseUrl: process.env.DATABASE_URL,
  apiToken: process.env.API_TOKEN,
  jwtSecret: process.env.JWT_SECRET,
  environment: process.env.NODE_ENV || "development"
};

// Validate required config
const required = ["databaseUrl", "apiToken", "jwtSecret"];
for (const key of required) {
  if (!config[key]) {
    throw new Error(`Missing required config: ${key}`);
  }
}

const mcpServer = new McpServer({
  name: "my-app",
  version: "1.0.0",
  config
});
```

---

## Testing Patterns

### Pattern 1: Unit Testing Tools

```javascript
const { describe, it, expect } = require("@jest/globals");

describe("greet tool", () => {
  it("should return greeting", async () => {
    const result = await greetTool({ name: "Alice" });

    expect(result.content[0].text).toBe("Hello, Alice!");
  });

  it("should handle empty name", async () => {
    const result = await greetTool({ name: "" });

    expect(result.isError).toBe(true);
  });
});
```

---

### Pattern 2: Integration Testing

```javascript
const request = require("supertest");

describe("MCP Server", () => {
  it("should handle tool call", async () => {
    const response = await request(app)
      .post("/mcp")
      .send({
        jsonrpc: "2.0",
        method: "tools/call",
        params: {
          name: "greet",
          arguments: { name: "Alice" }
        },
        id: 1
      });

    expect(response.status).toBe(200);
    expect(response.body.result.content[0].text).toContain("Alice");
  });
});
```

---

## Best Practices

1. **Tool Design**
   - Clear, descriptive names
   - Comprehensive input schemas
   - Meaningful descriptions for ChatGPT
   - Return structured content for widgets

2. **Error Handling**
   - Always catch errors
   - Return user-friendly messages
   - Log errors for debugging
   - Use `isError: true` flag

3. **State Management**
   - Use databases for persistence
   - Keep in-memory state minimal
   - Return authoritative state after mutations
   - Handle concurrent requests

4. **Authentication**
   - Verify tokens on every request
   - Check scopes and permissions
   - Return proper WWW-Authenticate headers
   - Implement token refresh

5. **Performance**
   - Use connection pooling
   - Implement caching where appropriate
   - Add timeouts to external calls
   - Monitor response times

6. **Security**
   - Validate all inputs
   - Sanitize user data
   - Use HTTPS in production
   - Implement rate limiting
   - Audit log sensitive operations
