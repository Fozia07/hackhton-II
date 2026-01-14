/**
 * Shadow Theme Configuration
 * Soft, multi-layer shadow system
 */

export const shadows = {
  light: {
    sm: '0 1px 2px 0 hsl(0 0% 0% / 0.04), 0 2px 4px 0 hsl(0 0% 0% / 0.04), 0 0 0 1px hsl(0 0% 0% / 0.02)',
    md: '0 2px 4px -1px hsl(0 0% 0% / 0.06), 0 4px 8px -1px hsl(0 0% 0% / 0.1), 0 0 0 1px hsl(0 0% 0% / 0.04)',
    lg: '0 4px 8px -2px hsl(0 0% 0% / 0.08), 0 8px 16px -2px hsl(0 0% 0% / 0.12), 0 0 0 1px hsl(0 0% 0% / 0.04)',
    xl: '0 8px 16px -4px hsl(0 0% 0% / 0.1), 0 16px 32px -4px hsl(0 0% 0% / 0.15), 0 0 0 1px hsl(0 0% 0% / 0.04)',
    '2xl': '0 16px 32px -8px hsl(0 0% 0% / 0.12), 0 32px 64px -8px hsl(0 0% 0% / 0.18), 0 0 0 1px hsl(0 0% 0% / 0.04)',
    inner: 'inset 0 2px 4px 0 hsl(0 0% 0% / 0.06)',
  },
  dark: {
    sm: '0 1px 2px 0 hsl(0 0% 0% / 0.3), 0 2px 4px 0 hsl(0 0% 0% / 0.3), 0 0 0 1px hsl(0 0% 100% / 0.05)',
    md: '0 2px 4px -1px hsl(0 0% 0% / 0.4), 0 4px 8px -1px hsl(0 0% 0% / 0.5), 0 0 0 1px hsl(0 0% 100% / 0.05)',
    lg: '0 4px 8px -2px hsl(0 0% 0% / 0.5), 0 8px 16px -2px hsl(0 0% 0% / 0.6), 0 0 0 1px hsl(0 0% 100% / 0.05)',
    xl: '0 8px 16px -4px hsl(0 0% 0% / 0.6), 0 16px 32px -4px hsl(0 0% 0% / 0.8), 0 0 0 1px hsl(0 0% 100% / 0.05)',
    '2xl': '0 16px 32px -8px hsl(0 0% 0% / 0.7), 0 32px 64px -8px hsl(0 0% 0% / 0.9), 0 0 0 1px hsl(0 0% 100% / 0.05)',
    inner: 'inset 0 2px 4px 0 hsl(0 0% 0% / 0.4)',
  },
  glassmorphism: {
    light: {
      background: 'hsl(0 0% 100% / 0.7)',
      border: 'hsl(0 0% 100% / 0.2)',
      fallback: 'hsl(0 0% 100% / 0.95)',
      modal: {
        background: 'hsl(0 0% 100% / 0.8)',
        border: 'hsl(0 0% 100% / 0.3)',
      },
    },
    dark: {
      background: 'hsl(210 18% 12% / 0.5)',
      border: 'hsl(0 0% 100% / 0.1)',
      fallback: 'hsl(210 18% 12% / 0.95)',
      modal: {
        background: 'hsl(210 18% 12% / 0.7)',
        border: 'hsl(0 0% 100% / 0.15)',
      },
    },
  },
} as const;

export type ShadowConfig = typeof shadows;
