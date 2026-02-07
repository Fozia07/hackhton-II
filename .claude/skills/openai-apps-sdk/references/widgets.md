# Widget Development

Comprehensive guide to building interactive widgets for ChatGPT using OpenAI Apps SDK.

---

## Widget Fundamentals

### What is a Widget?

A widget is an HTML/CSS/JS component that renders inline within ChatGPT conversations. Widgets:
- Display rich, interactive UI
- Access tool output data
- Call tools back to the MCP server
- Manage persistent state
- Respond to user interactions

### Widget Lifecycle

```
1. ChatGPT calls MCP tool
2. Tool returns structuredContent + widget metadata
3. ChatGPT loads widget HTML in iframe
4. Widget reads window.openai.toolOutput
5. Widget renders UI
6. User interacts with widget
7. Widget calls tools or updates state
8. Cycle repeats
```

---

## window.openai API

The bridge between your widget and ChatGPT.

### Available Properties

```javascript
// Data from MCP server
window.openai.toolOutput          // Structured content from tool
window.openai.widgetState         // Persisted widget state
window.openai.widgetSessionId     // Unique widget instance ID

// Environment info
window.openai.locale              // User's locale (e.g., "en-US")
window.openai.theme               // "light" or "dark"
window.openai.displayMode         // "inline", "pip", or "fullscreen"

// Capabilities
window.openai.capabilities        // Available features
```

### Available Methods

```javascript
// Call tools
await window.openai.callTool(toolName, args)

// State management
window.openai.setWidgetState(stateObject)

// Navigation
await window.openai.sendFollowUpMessage({ prompt: "..." })
window.openai.openExternal({ href: "https://..." })

// Display modes
await window.openai.requestDisplayMode({ mode: "fullscreen" })
```

---

## Basic Widget Patterns

### Pattern 1: Static Display Widget

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: system-ui, -apple-system, sans-serif;
      padding: 16px;
      margin: 0;
    }
    .card {
      background: white;
      border-radius: 8px;
      padding: 16px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .title {
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 8px;
    }
    .description {
      color: #666;
      line-height: 1.5;
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    // Read tool output
    const data = window.openai.toolOutput || {};

    // Render
    document.getElementById('app').innerHTML = `
      <div class="card">
        <div class="title">${data.title || 'No title'}</div>
        <div class="description">${data.description || 'No description'}</div>
      </div>
    `;
  </script>
</body>
</html>
```

---

### Pattern 2: Interactive Widget

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: system-ui; padding: 16px; }
    button {
      background: #0066cc;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }
    button:hover { background: #0052a3; }
    button:disabled {
      background: #ccc;
      cursor: not-allowed;
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    const data = window.openai.toolOutput || {};

    function render() {
      document.getElementById('app').innerHTML = `
        <h2>${data.title}</h2>
        <p>${data.message}</p>
        <button onclick="handleAction()">Take Action</button>
      `;
    }

    async function handleAction() {
      // Disable button
      const button = document.querySelector('button');
      button.disabled = true;
      button.textContent = 'Processing...';

      try {
        // Call tool
        await window.openai.callTool('process_action', {
          itemId: data.id
        });
      } catch (error) {
        console.error('Action failed:', error);
        button.disabled = false;
        button.textContent = 'Take Action';
      }
    }

    render();
  </script>
</body>
</html>
```

---

### Pattern 3: List Widget

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: system-ui; padding: 16px; }
    .list-item {
      padding: 12px;
      border-bottom: 1px solid #eee;
      cursor: pointer;
      transition: background 0.2s;
    }
    .list-item:hover { background: #f5f5f5; }
    .list-item.selected { background: #e3f2fd; }
    .empty { color: #999; text-align: center; padding: 32px; }
  </style>
</head>
<body>
  <div id="app"></div>
  <script>
    const items = window.openai.toolOutput?.items || [];
    let state = window.openai.widgetState || { selectedId: null };

    function render() {
      if (items.length === 0) {
        document.getElementById('app').innerHTML =
          '<div class="empty">No items to display</div>';
        return;
      }

      const html = items.map(item => `
        <div
          class="list-item ${state.selectedId === item.id ? 'selected' : ''}"
          onclick="selectItem('${item.id}')"
        >
          <strong>${item.title}</strong>
          <div style="color: #666; font-size: 14px;">${item.description}</div>
        </div>
      `).join('');

      document.getElementById('app').innerHTML = html;
    }

    function selectItem(id) {
      state.selectedId = id;
      window.openai.setWidgetState(state);
      render();
    }

    render();
  </script>
</body>
</html>
```

---

## State Management

### Pattern 1: Simple State

```javascript
// Initialize state
let state = window.openai.widgetState || {
  count: 0,
  items: []
};

// Update state
function updateState(updates) {
  state = { ...state, ...updates };
  window.openai.setWidgetState(state);
  render();
}

// Usage
updateState({ count: state.count + 1 });
```

---

### Pattern 2: Complex State

```javascript
class WidgetState {
  constructor() {
    this.state = window.openai.widgetState || this.getInitialState();
  }

  getInitialState() {
    return {
      selectedItems: [],
      filters: {},
      sortBy: 'name',
      viewMode: 'grid'
    };
  }

  get(key) {
    return this.state[key];
  }

  set(key, value) {
    this.state[key] = value;
    this.persist();
  }

  update(updates) {
    this.state = { ...this.state, ...updates };
    this.persist();
  }

  persist() {
    window.openai.setWidgetState(this.state);
  }
}

// Usage
const widgetState = new WidgetState();
widgetState.set('viewMode', 'list');
```

---

### Pattern 3: State with Validation

```javascript
const stateSchema = {
  selectedId: { type: 'string', nullable: true },
  page: { type: 'number', min: 1, default: 1 },
  filters: { type: 'object', default: {} }
};

function validateState(state) {
  const validated = {};

  for (const [key, schema] of Object.entries(stateSchema)) {
    const value = state[key];

    if (value === undefined || value === null) {
      validated[key] = schema.default;
      continue;
    }

    if (schema.type === 'number' && typeof value === 'number') {
      if (schema.min !== undefined && value < schema.min) {
        validated[key] = schema.min;
      } else {
        validated[key] = value;
      }
    } else if (typeof value === schema.type) {
      validated[key] = value;
    } else {
      validated[key] = schema.default;
    }
  }

  return validated;
}

// Initialize with validation
let state = validateState(window.openai.widgetState || {});

function updateState(updates) {
  state = validateState({ ...state, ...updates });
  window.openai.setWidgetState(state);
  render();
}
```

---

## Theme Support

### Pattern 1: CSS Variables

```html
<style>
  :root {
    --bg-primary: white;
    --bg-secondary: #f5f5f5;
    --text-primary: #000;
    --text-secondary: #666;
    --border-color: #ddd;
    --accent-color: #0066cc;
  }

  [data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2a2a2a;
    --text-primary: #fff;
    --text-secondary: #aaa;
    --border-color: #444;
    --accent-color: #4d9fff;
  }

  body {
    background: var(--bg-primary);
    color: var(--text-primary);
  }

  .card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
  }

  button {
    background: var(--accent-color);
    color: white;
  }
</style>

<script>
  // Apply theme
  const theme = window.openai.theme || 'light';
  document.documentElement.setAttribute('data-theme', theme);

  // Listen for theme changes
  if (window.openai.onThemeChange) {
    window.openai.onThemeChange((newTheme) => {
      document.documentElement.setAttribute('data-theme', newTheme);
    });
  }
</script>
```

---

### Pattern 2: Dynamic Theme Classes

```javascript
const themes = {
  light: {
    background: '#ffffff',
    text: '#000000',
    border: '#dddddd',
    accent: '#0066cc'
  },
  dark: {
    background: '#1a1a1a',
    text: '#ffffff',
    border: '#444444',
    accent: '#4d9fff'
  }
};

function applyTheme(themeName) {
  const theme = themes[themeName] || themes.light;

  document.body.style.background = theme.background;
  document.body.style.color = theme.text;

  // Apply to all elements with theme classes
  document.querySelectorAll('.themed').forEach(el => {
    el.style.borderColor = theme.border;
  });

  document.querySelectorAll('.accent').forEach(el => {
    el.style.background = theme.accent;
  });
}

// Apply current theme
applyTheme(window.openai.theme);
```

---

## Responsive Design

### Pattern 1: Mobile-First CSS

```css
/* Mobile first (default) */
body {
  padding: 12px;
  font-size: 14px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.button {
  width: 100%;
  padding: 12px;
  font-size: 16px; /* Larger for touch */
}

/* Tablet */
@media (min-width: 768px) {
  body {
    padding: 16px;
    font-size: 16px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .button {
    width: auto;
    padding: 10px 20px;
    font-size: 14px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  body {
    padding: 24px;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
}
```

---

### Pattern 2: JavaScript Responsive Handling

```javascript
function getDeviceType() {
  const width = window.innerWidth;

  if (width < 768) return 'mobile';
  if (width < 1024) return 'tablet';
  return 'desktop';
}

function render() {
  const deviceType = getDeviceType();
  const data = window.openai.toolOutput || {};

  if (deviceType === 'mobile') {
    renderMobileView(data);
  } else if (deviceType === 'tablet') {
    renderTabletView(data);
  } else {
    renderDesktopView(data);
  }
}

function renderMobileView(data) {
  document.getElementById('app').innerHTML = `
    <div class="mobile-layout">
      ${data.items.map(item => `
        <div class="mobile-card">${item.title}</div>
      `).join('')}
    </div>
  `;
}

// Handle resize
window.addEventListener('resize', () => {
  clearTimeout(window.resizeTimer);
  window.resizeTimer = setTimeout(render, 250);
});

render();
```

---

## Advanced Patterns

### Pattern 1: Form Widget

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: system-ui; padding: 16px; }
    .form-group { margin-bottom: 16px; }
    label {
      display: block;
      margin-bottom: 4px;
      font-weight: 500;
    }
    input, select, textarea {
      width: 100%;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 14px;
    }
    button {
      background: #0066cc;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 4px;
      cursor: pointer;
    }
    .error { color: #d32f2f; font-size: 12px; margin-top: 4px; }
  </style>
</head>
<body>
  <form id="myForm">
    <div class="form-group">
      <label for="name">Name</label>
      <input type="text" id="name" required>
      <div class="error" id="name-error"></div>
    </div>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" required>
      <div class="error" id="email-error"></div>
    </div>

    <div class="form-group">
      <label for="category">Category</label>
      <select id="category">
        <option value="">Select...</option>
        <option value="general">General</option>
        <option value="support">Support</option>
        <option value="feedback">Feedback</option>
      </select>
    </div>

    <div class="form-group">
      <label for="message">Message</label>
      <textarea id="message" rows="4" required></textarea>
    </div>

    <button type="submit">Submit</button>
  </form>

  <script>
    const form = document.getElementById('myForm');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Clear errors
      document.querySelectorAll('.error').forEach(el => el.textContent = '');

      // Get form data
      const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        category: document.getElementById('category').value,
        message: document.getElementById('message').value
      };

      // Validate
      let isValid = true;

      if (!formData.name.trim()) {
        document.getElementById('name-error').textContent = 'Name is required';
        isValid = false;
      }

      if (!formData.email.includes('@')) {
        document.getElementById('email-error').textContent = 'Invalid email';
        isValid = false;
      }

      if (!isValid) return;

      // Submit
      const button = form.querySelector('button');
      button.disabled = true;
      button.textContent = 'Submitting...';

      try {
        await window.openai.callTool('submit_form', formData);
        form.reset();
        alert('Form submitted successfully!');
      } catch (error) {
        alert('Submission failed. Please try again.');
      } finally {
        button.disabled = false;
        button.textContent = 'Submit';
      }
    });
  </script>
</body>
</html>
```

---

### Pattern 2: Pagination Widget

```javascript
const data = window.openai.toolOutput || {};
const items = data.items || [];
const itemsPerPage = 10;

let state = window.openai.widgetState || {
  currentPage: 1
};

function getTotalPages() {
  return Math.ceil(items.length / itemsPerPage);
}

function getCurrentPageItems() {
  const start = (state.currentPage - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return items.slice(start, end);
}

function goToPage(page) {
  const totalPages = getTotalPages();
  if (page < 1 || page > totalPages) return;

  state.currentPage = page;
  window.openai.setWidgetState(state);
  render();
}

function render() {
  const currentItems = getCurrentPageItems();
  const totalPages = getTotalPages();

  const itemsHtml = currentItems.map(item => `
    <div class="item">${item.title}</div>
  `).join('');

  const paginationHtml = `
    <div class="pagination">
      <button
        onclick="goToPage(${state.currentPage - 1})"
        ${state.currentPage === 1 ? 'disabled' : ''}
      >
        Previous
      </button>
      <span>Page ${state.currentPage} of ${totalPages}</span>
      <button
        onclick="goToPage(${state.currentPage + 1})"
        ${state.currentPage === totalPages ? 'disabled' : ''}
      >
        Next
      </button>
    </div>
  `;

  document.getElementById('app').innerHTML = itemsHtml + paginationHtml;
}

render();
```

---

### Pattern 3: Search/Filter Widget

```javascript
const allItems = window.openai.toolOutput?.items || [];

let state = window.openai.widgetState || {
  searchQuery: '',
  filterCategory: 'all',
  sortBy: 'name'
};

function getFilteredItems() {
  let filtered = allItems;

  // Search
  if (state.searchQuery) {
    const query = state.searchQuery.toLowerCase();
    filtered = filtered.filter(item =>
      item.title.toLowerCase().includes(query) ||
      item.description.toLowerCase().includes(query)
    );
  }

  // Filter by category
  if (state.filterCategory !== 'all') {
    filtered = filtered.filter(item => item.category === state.filterCategory);
  }

  // Sort
  filtered.sort((a, b) => {
    if (state.sortBy === 'name') {
      return a.title.localeCompare(b.title);
    } else if (state.sortBy === 'date') {
      return new Date(b.date) - new Date(a.date);
    }
    return 0;
  });

  return filtered;
}

function updateSearch(query) {
  state.searchQuery = query;
  window.openai.setWidgetState(state);
  render();
}

function updateFilter(category) {
  state.filterCategory = category;
  window.openai.setWidgetState(state);
  render();
}

function updateSort(sortBy) {
  state.sortBy = sortBy;
  window.openai.setWidgetState(state);
  render();
}

function render() {
  const items = getFilteredItems();

  document.getElementById('app').innerHTML = `
    <div class="controls">
      <input
        type="text"
        placeholder="Search..."
        value="${state.searchQuery}"
        oninput="updateSearch(this.value)"
      >

      <select onchange="updateFilter(this.value)">
        <option value="all" ${state.filterCategory === 'all' ? 'selected' : ''}>
          All Categories
        </option>
        <option value="tech" ${state.filterCategory === 'tech' ? 'selected' : ''}>
          Tech
        </option>
        <option value="business" ${state.filterCategory === 'business' ? 'selected' : ''}>
          Business
        </option>
      </select>

      <select onchange="updateSort(this.value)">
        <option value="name" ${state.sortBy === 'name' ? 'selected' : ''}>
          Sort by Name
        </option>
        <option value="date" ${state.sortBy === 'date' ? 'selected' : ''}>
          Sort by Date
        </option>
      </select>
    </div>

    <div class="results">
      ${items.length === 0 ? '<p>No results found</p>' : ''}
      ${items.map(item => `
        <div class="item">
          <h3>${item.title}</h3>
          <p>${item.description}</p>
        </div>
      `).join('')}
    </div>
  `;
}

render();
```

---

## Display Modes

### Pattern 1: Request Fullscreen

```javascript
async function goFullscreen() {
  try {
    const result = await window.openai.requestDisplayMode({
      mode: 'fullscreen'
    });

    if (result.mode === 'fullscreen') {
      renderFullscreenView();
    } else {
      console.log('Fullscreen not granted, got:', result.mode);
    }
  } catch (error) {
    console.error('Failed to request fullscreen:', error);
  }
}

function renderFullscreenView() {
  document.getElementById('app').innerHTML = `
    <div class="fullscreen-content">
      <h1>Fullscreen Mode</h1>
      <button onclick="exitFullscreen()">Exit Fullscreen</button>
    </div>
  `;
}

async function exitFullscreen() {
  await window.openai.requestDisplayMode({ mode: 'inline' });
  render();
}
```

---

### Pattern 2: Adaptive Layout

```javascript
function render() {
  const mode = window.openai.displayMode || 'inline';

  if (mode === 'fullscreen') {
    renderFullscreenLayout();
  } else if (mode === 'pip') {
    renderPipLayout();
  } else {
    renderInlineLayout();
  }
}

function renderFullscreenLayout() {
  // Large, detailed view
  document.getElementById('app').innerHTML = `
    <div class="fullscreen-layout">
      <header>Full Navigation</header>
      <main>Detailed Content</main>
      <aside>Sidebar</aside>
    </div>
  `;
}

function renderPipLayout() {
  // Compact, focused view
  document.getElementById('app').innerHTML = `
    <div class="pip-layout">
      <div>Essential Info Only</div>
    </div>
  `;
}

function renderInlineLayout() {
  // Standard inline view
  document.getElementById('app').innerHTML = `
    <div class="inline-layout">
      <div>Standard Content</div>
    </div>
  `;
}

render();
```

---

## Best Practices

### 1. Performance

- **Minimize DOM updates**: Batch changes, use virtual DOM if needed
- **Debounce user input**: Don't update on every keystroke
- **Lazy load images**: Use loading="lazy" attribute
- **Optimize bundle size**: Keep HTML/CSS/JS small
- **Use CSS animations**: Prefer CSS over JS for animations

### 2. Accessibility

- **Semantic HTML**: Use proper elements (button, nav, etc.)
- **ARIA labels**: Add aria-label for screen readers
- **Keyboard navigation**: Support Tab, Enter, Escape
- **Focus management**: Visible focus indicators
- **Color contrast**: Meet WCAG standards

### 3. User Experience

- **Loading states**: Show spinners during async operations
- **Error messages**: Clear, actionable error messages
- **Empty states**: Helpful messages when no data
- **Responsive**: Work on all screen sizes
- **Theme support**: Support light and dark themes

### 4. State Management

- **Keep state minimal**: Only persist what's necessary
- **Validate state**: Check types and values
- **Handle missing state**: Provide defaults
- **Token limits**: Keep state under 4k tokens

### 5. Security

- **Sanitize HTML**: Escape user input
- **Validate data**: Check all inputs
- **No sensitive data**: Don't store secrets in state
- **CSP compliance**: Follow content security policies

---

## Debugging

### Console Logging

```javascript
console.log('Tool output:', window.openai.toolOutput);
console.log('Widget state:', window.openai.widgetState);
console.log('Theme:', window.openai.theme);
console.log('Display mode:', window.openai.displayMode);
```

### Error Handling

```javascript
window.addEventListener('error', (event) => {
  console.error('Widget error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
});
```

### Testing Locally

```html
<script>
  // Mock window.openai for local testing
  if (!window.openai) {
    window.openai = {
      toolOutput: { /* mock data */ },
      widgetState: {},
      theme: 'light',
      displayMode: 'inline',
      callTool: async (name, args) => {
        console.log('Mock callTool:', name, args);
      },
      setWidgetState: (state) => {
        console.log('Mock setWidgetState:', state);
        window.openai.widgetState = state;
      }
    };
  }
</script>
```
