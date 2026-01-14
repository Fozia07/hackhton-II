# Data Model: Modern UI Enhancement Theme Configuration

**Feature**: Modern UI Enhancement
**Branch**: `001-ui-enhancement`
**Date**: 2026-01-14
**Phase**: Phase 1 - Design & Contracts

## Overview

This document defines the data entities and structures for the soft, professional theme configuration system. All entities are designed to support both light and dark modes while maintaining WCAG AA accessibility standards.

---

## Entity Definitions

### 1. ColorPalette

**Purpose**: Define complete color system for both light and dark themes

**Fields**:
- `name`: string - Palette identifier (e.g., "primary", "neutral", "success")
- `lightMode`: ColorScale - Color scale for light theme
- `darkMode`: ColorScale - Color scale for dark theme
- `description`: string - Usage description

**Validation Rules**:
- All colors must meet WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Each palette must have both lightMode and darkMode defined
- Color scales must have consistent step intervals

**Example**:
```typescript
interface ColorPalette {
  name: string;
  lightMode: ColorScale;
  darkMode: ColorScale;
  description: string;
}

const primaryPalette: ColorPalette = {
  name: "primary",
  lightMode: {
    50: "hsl(220, 40%, 98%)",
    100: "hsl(220, 38%, 95%)",
    // ... 200-900
  },
  darkMode: {
    50: "hsl(220, 38%, 12%)",
    100: "hsl(220, 36%, 16%)",
    // ... 200-900
  },
  description: "Soft blue/indigo for primary actions and brand elements"
};
```

---

### 2. ColorScale

**Purpose**: Provide consistent color tokens across application with state variations

**Fields**:
- `50-900`: string (HSL) - Color scale from lightest to darkest
- `base`: string (HSL) - Default color for the scale (typically 500)
- `hover`: string (HSL) - Hover state color (typically 600)
- `active`: string (HSL) - Active state color (typically 700)
- `disabled`: string (HSL) - Disabled state color (typically 300)

**State Variations**:
```typescript
interface ColorScale {
  50: string;   // Backgrounds
  100: string;  // Hover backgrounds
  200: string;  // Borders
  300: string;  // Disabled states
  400: string;  // Muted text
  500: string;  // Default - base color
  600: string;  // Hover - darker/lighter
  700: string;  // Active - even darker/lighter
  800: string;  // Text
  900: string;  // Headings
}

interface ColorStates {
  base: string;     // Default state
  hover: string;    // Hover state
  active: string;   // Active/pressed state
  disabled: string; // Disabled state
}
```

**Validation Rules**:
- All HSL values must be valid CSS color strings
- Contrast ratios must meet WCAG AA standards when used on appropriate backgrounds
- Hover state must be visibly different from base (minimum 10% lightness change)
- Active state must be visibly different from hover (minimum 10% lightness change)

**Semantic Color Scales**:
```typescript
interface SemanticColors {
  success: ColorStates;  // Soft green for positive actions
  warning: ColorStates;  // Soft amber for caution
  error: ColorStates;    // Soft red for errors
  info: ColorStates;     // Soft blue for information
}
```

---

### 3. AnimationPreset

**Purpose**: Define reusable animation configurations for consistent motion design

**Fields**:
- `name`: string - Preset identifier (e.g., "gentle-fade", "light-slide")
- `duration`: number - Animation duration in milliseconds (200-400ms)
- `easing`: string | number[] - Easing function (CSS or cubic-bezier array)
- `delay`: number - Optional delay in milliseconds
- `type`: "tween" | "spring" - Animation type for Framer Motion

**Spring-Specific Fields** (when type = "spring"):
- `stiffness`: number - Spring stiffness (100-300)
- `damping`: number - Spring damping (20-30)
- `mass`: number - Spring mass (0.8-1.2)

**Validation Rules**:
- Duration must be between 150ms and 500ms (prefer 200-400ms for light feel)
- Easing must be valid CSS easing or cubic-bezier array
- Spring values must create gentle, non-bouncy motion

**Example**:
```typescript
interface AnimationPreset {
  name: string;
  duration: number;
  easing: string | [number, number, number, number];
  delay?: number;
  type: "tween" | "spring";
  // Spring-specific
  stiffness?: number;
  damping?: number;
  mass?: number;
}

const gentleFade: AnimationPreset = {
  name: "gentle-fade",
  duration: 300,
  easing: [0.65, 0, 0.35, 1],
  type: "tween"
};

const springGentle: AnimationPreset = {
  name: "spring-gentle",
  duration: 0, // Calculated by spring physics
  easing: "linear",
  type: "spring",
  stiffness: 200,
  damping: 25,
  mass: 1
};
```

**Common Presets**:
```typescript
interface AnimationPresets {
  quick: AnimationPreset;      // 150-200ms for micro-interactions
  gentle: AnimationPreset;     // 250ms for most transitions
  smooth: AnimationPreset;     // 300ms for refined feel
  springGentle: AnimationPreset; // Natural spring motion
}
```

---

### 4. ShadowDefinition

**Purpose**: Define soft shadow system for elevation hierarchy

**Fields**:
- `name`: string - Shadow identifier (e.g., "soft-sm", "soft-md")
- `elevation`: number - Elevation level (0-5)
- `layers`: ShadowLayer[] - Array of shadow layers (ambient + direct + border)

**ShadowLayer Fields**:
- `x`: number - Horizontal offset in pixels
- `y`: number - Vertical offset in pixels
- `blur`: number - Blur radius in pixels
- `spread`: number - Spread radius in pixels
- `color`: string - Shadow color (RGBA)
- `opacity`: number - Shadow opacity (0-1)

**Validation Rules**:
- Shadows must use soft colors (not pure black)
- Opacity must be between 0.02 and 0.3 for light mode
- Opacity must be between 0.3 and 0.8 for dark mode
- Must include at least 2 layers (ambient + direct)
- Blur radius must scale proportionally with elevation

**Example**:
```typescript
interface ShadowLayer {
  x: number;
  y: number;
  blur: number;
  spread: number;
  color: string;
  opacity: number;
}

interface ShadowDefinition {
  name: string;
  elevation: number;
  layers: ShadowLayer[];
}

const softMedium: ShadowDefinition = {
  name: "soft-md",
  elevation: 2,
  layers: [
    // Ambient shadow
    { x: 0, y: 2, blur: 4, spread: -1, color: "rgb(0, 0, 0)", opacity: 0.06 },
    // Direct shadow
    { x: 0, y: 4, blur: 8, spread: -1, color: "rgb(0, 0, 0)", opacity: 0.1 },
    // Larger ambient
    { x: 0, y: 8, blur: 16, spread: -1, color: "rgb(0, 0, 0)", opacity: 0.1 }
  ]
};
```

**Shadow Scale**:
```typescript
interface ShadowScale {
  xs: ShadowDefinition;   // Elevation 0 - Subtle hover
  sm: ShadowDefinition;   // Elevation 1 - Cards at rest
  md: ShadowDefinition;   // Elevation 2 - Elevated cards
  lg: ShadowDefinition;   // Elevation 3 - Modals, popovers
  xl: ShadowDefinition;   // Elevation 4 - Dialogs
  "2xl": ShadowDefinition; // Elevation 5 - Full-screen overlays
}
```

**Dark Mode Shadows**:
```typescript
interface DarkModeShadow extends ShadowDefinition {
  lightBorder?: {
    width: number;
    color: string;
    opacity: number;
  };
}
```

---

### 5. ComponentVariant

**Purpose**: Define visual states for all interactive components

**Fields**:
- `component`: string - Component name (e.g., "Button", "Card", "Input")
- `variant`: string - Variant name (e.g., "primary", "secondary", "outline")
- `baseStyles`: StyleDefinition - Default state styles
- `hoverStyles`: StyleDefinition - Hover state styles
- `activeStyles`: StyleDefinition - Active/pressed state styles
- `focusStyles`: StyleDefinition - Focus state styles (keyboard navigation)
- `disabledStyles`: StyleDefinition - Disabled state styles

**StyleDefinition Fields**:
- `background`: string - Background color
- `color`: string - Text color
- `border`: string - Border style
- `shadow`: string - Box shadow reference
- `transform`: string - CSS transform
- `opacity`: number - Opacity value

**Validation Rules**:
- Hover states must be obviously different from base (user requirement)
- Focus states must have 3:1 contrast ratio with adjacent colors
- Disabled states must maintain 3:1 contrast for text
- All states must work in both light and dark modes

**Example**:
```typescript
interface StyleDefinition {
  background: string;
  color: string;
  border?: string;
  shadow?: string;
  transform?: string;
  opacity?: number;
}

interface ComponentVariant {
  component: string;
  variant: string;
  baseStyles: StyleDefinition;
  hoverStyles: StyleDefinition;
  activeStyles: StyleDefinition;
  focusStyles: StyleDefinition;
  disabledStyles: StyleDefinition;
}

const primaryButton: ComponentVariant = {
  component: "Button",
  variant: "primary",
  baseStyles: {
    background: "var(--primary-600)",
    color: "var(--white)",
    shadow: "var(--shadow-sm)",
    transform: "scale(1)"
  },
  hoverStyles: {
    background: "var(--primary-700)",
    color: "var(--white)",
    shadow: "var(--shadow-md)",
    transform: "scale(1.05)"
  },
  activeStyles: {
    background: "var(--primary-800)",
    color: "var(--white)",
    shadow: "var(--shadow-sm)",
    transform: "scale(0.98)"
  },
  focusStyles: {
    background: "var(--primary-600)",
    color: "var(--white)",
    border: "2px solid var(--primary-400)",
    shadow: "0 0 0 2px var(--primary-400), 0 0 0 4px var(--background)"
  },
  disabledStyles: {
    background: "var(--primary-300)",
    color: "var(--primary-100)",
    opacity: 0.6,
    transform: "scale(1)"
  }
};
```

---

### 6. GlassmorphismConfig

**Purpose**: Define subtle glassmorphism effects for elevated elements

**Fields**:
- `name`: string - Config identifier (e.g., "glass-subtle", "glass-modal")
- `backdropBlur`: number - Blur amount in pixels (4-16px)
- `backdropSaturate`: number - Saturation percentage (150-200%)
- `backgroundColor`: string - Semi-transparent background (RGBA)
- `borderColor`: string - Semi-transparent border (RGBA)
- `opacity`: number - Overall opacity (0.05-0.2)
- `fallbackBackground`: string - Solid background for unsupported browsers

**Validation Rules**:
- Blur values must be between 4px and 16px (performance)
- Background opacity must be between 0.05 and 0.2
- Must include fallback for browsers without backdrop-filter support
- Text over glassmorphic backgrounds must meet WCAG AA contrast

**Example**:
```typescript
interface GlassmorphismConfig {
  name: string;
  backdropBlur: number;
  backdropSaturate: number;
  backgroundColor: string;
  borderColor: string;
  opacity: number;
  fallbackBackground: string;
}

const glassSubtle: GlassmorphismConfig = {
  name: "glass-subtle",
  backdropBlur: 8,
  backdropSaturate: 180,
  backgroundColor: "rgba(255, 255, 255, 0.1)",
  borderColor: "rgba(255, 255, 255, 0.18)",
  opacity: 1,
  fallbackBackground: "rgba(255, 255, 255, 0.9)"
};

const glassModal: GlassmorphismConfig = {
  name: "glass-modal",
  backdropBlur: 12,
  backdropSaturate: 180,
  backgroundColor: "rgba(255, 255, 255, 0.15)",
  borderColor: "rgba(255, 255, 255, 0.2)",
  opacity: 1,
  fallbackBackground: "rgba(255, 255, 255, 0.95)"
};
```

**Component-Specific Configs**:
```typescript
interface GlassmorphismConfigs {
  modal: GlassmorphismConfig;
  navbar: GlassmorphismConfig;
  dropdown: GlassmorphismConfig;
  tooltip: GlassmorphismConfig;
}
```

---

## Relationships Between Entities

```
ColorPalette
  ├── lightMode: ColorScale
  │   ├── base (500)
  │   ├── hover (600)
  │   ├── active (700)
  │   └── disabled (300)
  └── darkMode: ColorScale
      ├── base (500)
      ├── hover (600)
      ├── active (700)
      └── disabled (300)

ComponentVariant
  ├── baseStyles: StyleDefinition
  │   ├── background → ColorPalette
  │   └── shadow → ShadowDefinition
  ├── hoverStyles: StyleDefinition
  │   ├── background → ColorPalette.hover
  │   ├── shadow → ShadowDefinition (elevated)
  │   └── transform → AnimationPreset
  ├── activeStyles: StyleDefinition
  ├── focusStyles: StyleDefinition
  └── disabledStyles: StyleDefinition

GlassmorphismConfig
  ├── backgroundColor → ColorPalette (with opacity)
  ├── borderColor → ColorPalette (with opacity)
  └── fallbackBackground → ColorPalette (solid)
```

---

## Theme Configuration Structure

```typescript
interface ThemeConfig {
  colors: {
    primary: ColorPalette;
    secondary: ColorPalette;
    neutral: ColorPalette;
    accent: ColorPalette;
    semantic: {
      success: ColorPalette;
      warning: ColorPalette;
      error: ColorPalette;
      info: ColorPalette;
    };
  };

  animations: {
    presets: AnimationPresets;
    transitions: {
      quick: AnimationPreset;
      gentle: AnimationPreset;
      smooth: AnimationPreset;
      springGentle: AnimationPreset;
    };
  };

  shadows: {
    light: ShadowScale;
    dark: ShadowScale;
  };

  components: {
    Button: ComponentVariant[];
    Card: ComponentVariant[];
    Input: ComponentVariant[];
    Modal: ComponentVariant[];
    // ... other components
  };

  glassmorphism: GlassmorphismConfigs;
}
```

---

## Usage Examples

### Accessing Color Values
```typescript
// Get primary button color
const buttonBg = theme.colors.primary.lightMode[600];

// Get hover state
const buttonHoverBg = theme.colors.primary.lightMode[700];

// Get semantic color
const successColor = theme.colors.semantic.success.lightMode.base;
```

### Applying Animation Presets
```typescript
// Use gentle animation
const transition = theme.animations.presets.gentle;

// Apply to Framer Motion
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={transition}
/>
```

### Using Shadow Definitions
```typescript
// Get medium shadow
const cardShadow = theme.shadows.light.md;

// Apply to component
<div style={{ boxShadow: cardShadow }} />
```

### Applying Component Variants
```typescript
// Get primary button variant
const primaryBtn = theme.components.Button.find(v => v.variant === "primary");

// Apply styles
<button
  className={cn(
    primaryBtn.baseStyles,
    "hover:" + primaryBtn.hoverStyles,
    "active:" + primaryBtn.activeStyles
  )}
/>
```

---

## Validation and Testing

### Color Contrast Validation
```typescript
function validateColorContrast(
  foreground: string,
  background: string,
  minRatio: number = 4.5
): boolean {
  const ratio = calculateContrastRatio(foreground, background);
  return ratio >= minRatio;
}
```

### Animation Duration Validation
```typescript
function validateAnimationDuration(duration: number): boolean {
  return duration >= 150 && duration <= 500;
}
```

### Shadow Opacity Validation
```typescript
function validateShadowOpacity(
  opacity: number,
  mode: "light" | "dark"
): boolean {
  if (mode === "light") {
    return opacity >= 0.02 && opacity <= 0.3;
  }
  return opacity >= 0.3 && opacity <= 0.8;
}
```

---

## Next Steps

1. Generate JSON contract files in `contracts/` directory
2. Implement theme configuration in TypeScript
3. Create Tailwind CSS configuration based on data model
4. Generate CSS custom properties for runtime theme switching
5. Create component variant implementations
