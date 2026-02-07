# Apps SDK UI Components

Comprehensive guide to using OpenAI Apps SDK UI design system with React and Tailwind CSS.

---

## Overview

Apps SDK UI is a lightweight, accessible design system providing:
- **Pre-built React components** (Button, Badge, Card, Input, etc.)
- **100+ icons** for common use cases
- **Design tokens** for colors, spacing, typography
- **Tailwind CSS integration** for custom styling
- **Theme support** (light/dark)
- **Responsive design** (mobile-first)
- **WCAG accessibility** compliance

---

## Installation

### Setup

```bash
# Install packages
npm install @openai/apps-sdk-ui react react-dom

# Install Tailwind CSS
npm install -D tailwindcss
```

### Configure Tailwind

**tailwind.config.js**:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./node_modules/@openai/apps-sdk-ui/**/*.{js,jsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Import Styles

**main.css**:
```css
@import "tailwindcss";
@import "@openai/apps-sdk-ui/css";

/* Required for Tailwind to find class references in Apps SDK UI */
@source "../node_modules/@openai/apps-sdk-ui";

/* Your custom styles */
```

---

## Core Components

### Button

```tsx
import { Button } from "@openai/apps-sdk-ui/components/Button"

// Basic button
<Button>Click me</Button>

// Variants
<Button variant="solid">Solid</Button>
<Button variant="soft">Soft</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>

// Colors
<Button color="primary">Primary</Button>
<Button color="secondary">Secondary</Button>
<Button color="success">Success</Button>
<Button color="danger">Danger</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>

// States
<Button disabled>Disabled</Button>
<Button loading>Loading</Button>

// Full width
<Button block>Full Width</Button>

// With icon
import { Plus } from "@openai/apps-sdk-ui/components/Icon"
<Button>
  <Plus />
  Add Item
</Button>
```

---

### Badge

```tsx
import { Badge } from "@openai/apps-sdk-ui/components/Badge"

// Basic badge
<Badge>New</Badge>

// Colors
<Badge color="primary">Primary</Badge>
<Badge color="success">Success</Badge>
<Badge color="warning">Warning</Badge>
<Badge color="danger">Danger</Badge>
<Badge color="neutral">Neutral</Badge>

// Sizes
<Badge size="sm">Small</Badge>
<Badge size="md">Medium</Badge>
<Badge size="lg">Large</Badge>

// Variants
<Badge variant="solid">Solid</Badge>
<Badge variant="soft">Soft</Badge>
<Badge variant="outline">Outline</Badge>

// With dot
<Badge dot>Status</Badge>
```

---

### Card

```tsx
import { Card } from "@openai/apps-sdk-ui/components/Card"

// Basic card
<Card>
  <h2>Card Title</h2>
  <p>Card content goes here</p>
</Card>

// With padding variants
<Card padding="none">No padding</Card>
<Card padding="sm">Small padding</Card>
<Card padding="md">Medium padding</Card>
<Card padding="lg">Large padding</Card>

// Interactive card
<Card interactive onClick={() => console.log('clicked')}>
  Clickable card
</Card>

// Custom styling
<Card className="shadow-lg border-2">
  Custom styled card
</Card>
```

---

### Input

```tsx
import { Input } from "@openai/apps-sdk-ui/components/Input"

// Basic input
<Input placeholder="Enter text..." />

// With label
<Input label="Name" placeholder="Your name" />

// Types
<Input type="text" />
<Input type="email" />
<Input type="password" />
<Input type="number" />

// States
<Input disabled placeholder="Disabled" />
<Input error="This field is required" />

// Sizes
<Input size="sm" />
<Input size="md" />
<Input size="lg" />

// With icon
import { Search } from "@openai/apps-sdk-ui/components/Icon"
<Input
  icon={<Search />}
  placeholder="Search..."
/>

// Controlled input
const [value, setValue] = useState('')
<Input
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>
```

---

### Select

```tsx
import { Select } from "@openai/apps-sdk-ui/components/Select"

// Basic select
<Select>
  <option value="">Select an option</option>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
  <option value="3">Option 3</option>
</Select>

// With label
<Select label="Category">
  <option value="">Choose category</option>
  <option value="tech">Technology</option>
  <option value="business">Business</option>
</Select>

// States
<Select disabled>
  <option>Disabled</option>
</Select>

<Select error="Please select an option">
  <option value="">Select...</option>
</Select>

// Controlled
const [value, setValue] = useState('')
<Select value={value} onChange={(e) => setValue(e.target.value)}>
  <option value="">Select...</option>
  <option value="1">Option 1</option>
</Select>
```

---

### Textarea

```tsx
import { Textarea } from "@openai/apps-sdk-ui/components/Textarea"

// Basic textarea
<Textarea placeholder="Enter your message..." />

// With label
<Textarea
  label="Message"
  placeholder="Type here..."
  rows={4}
/>

// States
<Textarea disabled placeholder="Disabled" />
<Textarea error="Message is required" />

// Controlled
const [value, setValue] = useState('')
<Textarea
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>
```

---

### Checkbox

```tsx
import { Checkbox } from "@openai/apps-sdk-ui/components/Checkbox"

// Basic checkbox
<Checkbox label="Accept terms" />

// Controlled
const [checked, setChecked] = useState(false)
<Checkbox
  checked={checked}
  onChange={(e) => setChecked(e.target.checked)}
  label="Subscribe to newsletter"
/>

// States
<Checkbox disabled label="Disabled" />
<Checkbox indeterminate label="Indeterminate" />

// Without label
<Checkbox />
```

---

### Radio

```tsx
import { Radio } from "@openai/apps-sdk-ui/components/Radio"

// Radio group
const [selected, setSelected] = useState('option1')

<div>
  <Radio
    name="options"
    value="option1"
    checked={selected === 'option1'}
    onChange={(e) => setSelected(e.target.value)}
    label="Option 1"
  />
  <Radio
    name="options"
    value="option2"
    checked={selected === 'option2'}
    onChange={(e) => setSelected(e.target.value)}
    label="Option 2"
  />
  <Radio
    name="options"
    value="option3"
    checked={selected === 'option3'}
    onChange={(e) => setSelected(e.target.value)}
    label="Option 3"
  />
</div>
```

---

### Switch

```tsx
import { Switch } from "@openai/apps-sdk-ui/components/Switch"

// Basic switch
<Switch label="Enable notifications" />

// Controlled
const [enabled, setEnabled] = useState(false)
<Switch
  checked={enabled}
  onChange={(e) => setEnabled(e.target.checked)}
  label="Dark mode"
/>

// States
<Switch disabled label="Disabled" />

// Sizes
<Switch size="sm" label="Small" />
<Switch size="md" label="Medium" />
<Switch size="lg" label="Large" />
```

---

## Icons

### Available Icons

```tsx
import {
  // Actions
  Plus, Minus, Check, X, Edit, Trash, Copy, Download, Upload,

  // Navigation
  ChevronLeft, ChevronRight, ChevronUp, ChevronDown,
  ArrowLeft, ArrowRight, ArrowUp, ArrowDown,

  // UI
  Search, Filter, Settings, Menu, Close, Info, Warning, Error,

  // Communication
  Mail, Phone, Message, Bell, Send,

  // Media
  Image, Video, Music, File, Folder,

  // Social
  Heart, Star, Share, Bookmark, Like,

  // Business
  Calendar, Clock, Invoice, Members, Maps,

  // And 70+ more...
} from "@openai/apps-sdk-ui/components/Icon"

// Usage
<Plus className="size-4" />
<Search className="size-6 text-blue-500" />
<Heart className="size-8" />
```

### Icon Sizes

```tsx
// Using Tailwind size utilities
<Icon className="size-3" />  // 12px
<Icon className="size-4" />  // 16px
<Icon className="size-5" />  // 20px
<Icon className="size-6" />  // 24px
<Icon className="size-8" />  // 32px
<Icon className="size-10" /> // 40px

// Custom size
<Icon className="w-12 h-12" />
```

### Icon Colors

```tsx
// Using Tailwind color utilities
<Icon className="text-primary" />
<Icon className="text-secondary" />
<Icon className="text-success" />
<Icon className="text-danger" />
<Icon className="text-blue-500" />
```

---

## Layout Components

### Stack

```tsx
import { Stack } from "@openai/apps-sdk-ui/components/Stack"

// Vertical stack (default)
<Stack spacing="md">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</Stack>

// Horizontal stack
<Stack direction="horizontal" spacing="sm">
  <Button>Button 1</Button>
  <Button>Button 2</Button>
</Stack>

// Spacing options
<Stack spacing="xs">...</Stack>  // 4px
<Stack spacing="sm">...</Stack>  // 8px
<Stack spacing="md">...</Stack>  // 16px
<Stack spacing="lg">...</Stack>  // 24px
<Stack spacing="xl">...</Stack>  // 32px

// Alignment
<Stack align="start">...</Stack>
<Stack align="center">...</Stack>
<Stack align="end">...</Stack>
```

---

### Grid

```tsx
import { Grid } from "@openai/apps-sdk-ui/components/Grid"

// Basic grid
<Grid cols={3} gap="md">
  <Card>Item 1</Card>
  <Card>Item 2</Card>
  <Card>Item 3</Card>
</Grid>

// Responsive columns
<Grid
  cols={{ mobile: 1, tablet: 2, desktop: 3 }}
  gap="lg"
>
  <Card>Item 1</Card>
  <Card>Item 2</Card>
  <Card>Item 3</Card>
</Grid>

// Custom gap
<Grid cols={2} gap="sm">...</Grid>
```

---

## Complete Examples

### Example 1: Reservation Card

```tsx
import { Badge } from "@openai/apps-sdk-ui/components/Badge"
import { Button } from "@openai/apps-sdk-ui/components/Button"
import {
  Calendar,
  Invoice,
  Maps,
  Members,
  Phone,
} from "@openai/apps-sdk-ui/components/Icon"

export function ReservationCard() {
  return (
    <div className="w-full max-w-sm rounded-2xl border border-default bg-surface shadow-lg p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-secondary text-sm">Reservation</p>
          <h2 className="mt-1 heading-lg">La Luna Bistro</h2>
        </div>
        <Badge color="success">Confirmed</Badge>
      </div>

      <div>
        <dl className="mt-4 grid grid-cols-[auto_1fr] gap-x-3 gap-y-2 text-sm">
          <dt className="flex items-center gap-1.5 font-medium text-secondary">
            <Calendar className="size-4" />
            Date
          </dt>
          <dd className="text-right">Apr 12 · 7:30 PM</dd>

          <dt className="flex items-center gap-1.5 font-medium text-secondary">
            <Members className="size-4" />
            Guests
          </dt>
          <dd className="text-right">Party of 2</dd>

          <dt className="flex items-center gap-1.5 font-medium text-secondary">
            <Invoice className="size-4" />
            Reference
          </dt>
          <dd className="text-right uppercase">4F9Q2K</dd>
        </dl>
      </div>

      <div className="mt-4 grid gap-3 border-t border-subtle pt-4 sm:grid-cols-2">
        <Button variant="soft" color="secondary" block>
          <Phone />
          Call
        </Button>
        <Button color="primary" block>
          <Maps />
          Directions
        </Button>
      </div>
    </div>
  )
}
```

---

### Example 2: User Profile Card

```tsx
import { Badge } from "@openai/apps-sdk-ui/components/Badge"
import { Button } from "@openai/apps-sdk-ui/components/Button"
import { Card } from "@openai/apps-sdk-ui/components/Card"
import { Mail, Phone, Edit } from "@openai/apps-sdk-ui/components/Icon"

export function UserProfileCard({ user }) {
  return (
    <Card>
      <div className="flex items-start gap-4">
        <img
          src={user.avatar}
          alt={user.name}
          className="size-16 rounded-full"
        />
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h3 className="heading-md">{user.name}</h3>
            <Badge color="success" size="sm">Active</Badge>
          </div>
          <p className="text-secondary text-sm">{user.role}</p>
        </div>
        <Button variant="ghost" size="sm">
          <Edit />
        </Button>
      </div>

      <div className="mt-4 space-y-2">
        <div className="flex items-center gap-2 text-sm">
          <Mail className="size-4 text-secondary" />
          <span>{user.email}</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <Phone className="size-4 text-secondary" />
          <span>{user.phone}</span>
        </div>
      </div>

      <div className="mt-4 flex gap-2">
        <Button variant="soft" block>Message</Button>
        <Button color="primary" block>View Profile</Button>
      </div>
    </Card>
  )
}
```

---

### Example 3: Search Form

```tsx
import { useState } from "react"
import { Button } from "@openai/apps-sdk-ui/components/Button"
import { Input } from "@openai/apps-sdk-ui/components/Input"
import { Select } from "@openai/apps-sdk-ui/components/Select"
import { Search, Filter } from "@openai/apps-sdk-ui/components/Icon"

export function SearchForm({ onSearch }) {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('')
  const [sortBy, setSortBy] = useState('relevance')

  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch({ query, category, sortBy })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        icon={<Search />}
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div className="grid grid-cols-2 gap-4">
        <Select
          label="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          <option value="tech">Technology</option>
          <option value="business">Business</option>
          <option value="design">Design</option>
        </Select>

        <Select
          label="Sort By"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <option value="relevance">Relevance</option>
          <option value="date">Date</option>
          <option value="popularity">Popularity</option>
        </Select>
      </div>

      <Button type="submit" block>
        <Filter />
        Search
      </Button>
    </form>
  )
}
```

---

### Example 4: Settings Panel

```tsx
import { useState } from "react"
import { Card } from "@openai/apps-sdk-ui/components/Card"
import { Switch } from "@openai/apps-sdk-ui/components/Switch"
import { Select } from "@openai/apps-sdk-ui/components/Select"
import { Button } from "@openai/apps-sdk-ui/components/Button"

export function SettingsPanel() {
  const [notifications, setNotifications] = useState(true)
  const [darkMode, setDarkMode] = useState(false)
  const [language, setLanguage] = useState('en')

  const handleSave = () => {
    // Save settings
    console.log({ notifications, darkMode, language })
  }

  return (
    <Card>
      <h2 className="heading-lg mb-4">Settings</h2>

      <div className="space-y-4">
        <Switch
          checked={notifications}
          onChange={(e) => setNotifications(e.target.checked)}
          label="Enable notifications"
        />

        <Switch
          checked={darkMode}
          onChange={(e) => setDarkMode(e.target.checked)}
          label="Dark mode"
        />

        <Select
          label="Language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="en">English</option>
          <option value="es">Español</option>
          <option value="fr">Français</option>
          <option value="de">Deutsch</option>
        </Select>

        <div className="flex gap-2 pt-4 border-t">
          <Button variant="outline" block>Cancel</Button>
          <Button color="primary" block onClick={handleSave}>
            Save Changes
          </Button>
        </div>
      </div>
    </Card>
  )
}
```

---

## Design Tokens

### Colors

```css
/* Semantic colors */
--color-primary
--color-secondary
--color-success
--color-warning
--color-danger
--color-neutral

/* Text colors */
--color-text-primary
--color-text-secondary
--color-text-tertiary

/* Background colors */
--color-bg-surface
--color-bg-default
--color-bg-subtle

/* Border colors */
--color-border-default
--color-border-subtle
```

### Tailwind Classes

```tsx
// Text colors
<p className="text-primary">Primary text</p>
<p className="text-secondary">Secondary text</p>
<p className="text-tertiary">Tertiary text</p>

// Background colors
<div className="bg-surface">Surface background</div>
<div className="bg-default">Default background</div>

// Border colors
<div className="border border-default">Default border</div>
<div className="border border-subtle">Subtle border</div>
```

### Typography

```tsx
// Headings
<h1 className="heading-xl">Extra Large Heading</h1>
<h2 className="heading-lg">Large Heading</h2>
<h3 className="heading-md">Medium Heading</h3>
<h4 className="heading-sm">Small Heading</h4>

// Body text
<p className="text-base">Base text</p>
<p className="text-sm">Small text</p>
<p className="text-xs">Extra small text</p>

// Font weights
<p className="font-normal">Normal weight</p>
<p className="font-medium">Medium weight</p>
<p className="font-semibold">Semibold weight</p>
<p className="font-bold">Bold weight</p>
```

### Spacing

```tsx
// Padding
<div className="p-2">8px padding</div>
<div className="p-4">16px padding</div>
<div className="p-6">24px padding</div>
<div className="p-8">32px padding</div>

// Margin
<div className="m-2">8px margin</div>
<div className="m-4">16px margin</div>

// Gap
<div className="flex gap-2">8px gap</div>
<div className="flex gap-4">16px gap</div>
```

---

## Theme Support

### Using Theme Classes

```tsx
// Component adapts to theme automatically
<Button color="primary">Themed Button</Button>

// Custom theme-aware styling
<div className="bg-surface text-primary border border-default">
  This adapts to light/dark theme
</div>
```

### Detecting Theme

```tsx
import { useEffect, useState } from 'react'

function useTheme() {
  const [theme, setTheme] = useState(window.openai?.theme || 'light')

  useEffect(() => {
    if (window.openai?.onThemeChange) {
      window.openai.onThemeChange(setTheme)
    }
  }, [])

  return theme
}

// Usage
function MyComponent() {
  const theme = useTheme()

  return (
    <div>
      Current theme: {theme}
    </div>
  )
}
```

---

## Best Practices

### 1. Component Usage

- Use semantic components (Button, not div with onClick)
- Leverage built-in variants and colors
- Use icons from the icon library
- Follow spacing conventions

### 2. Styling

- Use Tailwind utilities for custom styling
- Use design tokens for consistency
- Support both light and dark themes
- Make components responsive

### 3. Accessibility

- Use proper ARIA labels
- Ensure keyboard navigation works
- Maintain color contrast ratios
- Test with screen readers

### 4. Performance

- Import only components you use
- Optimize bundle size
- Use lazy loading for large components
- Minimize re-renders

---

## Troubleshooting

### Styles Not Applying

**Check**:
- Tailwind config includes Apps SDK UI path
- CSS imports are in correct order
- `@source` directive is present

### Icons Not Showing

**Check**:
- Icon component is imported correctly
- Size class is applied (e.g., `className="size-4"`)
- Icon name is correct

### Theme Not Working

**Check**:
- Using semantic color classes (text-primary, not text-blue-500)
- Design tokens are imported
- Theme detection is implemented
