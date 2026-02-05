/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');

export default {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // SaaS-style theme colors as specified
        // Light Mode Colors
        background: '#F8FAFC',      // Soft neutral background
        card: '#FFFFFF',            // White cards
        primary: '#2563EB',         // Slate blue primary accent
        'primary-foreground': '#F8FAFC',
        'primary-light': '#dbeafe', // Lighter shade for hover states
        'primary-dark': '#1d4ed8',  // Darker shade for active states
        'text-primary': '#0F172A',  // Dark slate text
        'text-muted': '#64748B',    // Gray muted text
        border: '#E2E8F0',          // Subtle gray borders
        success: '#22C55E',         // Green for completed tasks
        warning: '#F59E0B',         // Amber for update actions
        // Dark Mode Colors
        'dark-background': '#020617',     // Charcoal background
        'dark-card': '#0F172A',           // Deep slate cards
        'dark-primary': '#3B82F6',        // Electric blue primary
        'dark-text-primary': '#E5E7EB',   // Light gray text
        'dark-text-muted': '#94A3B8',     // Muted text in dark mode
        'dark-border': '#1E293B',         // Dark borders
        // Semantic colors for dynamic theming
        'light-mode': {
          background: '#F8FAFC',
          card: '#FFFFFF',
          primary: '#2563EB',
          'primary-foreground': '#F8FAFC',
          'text-primary': '#0F172A',
          'text-muted': '#64748B',
          border: '#E2E8F0',
          success: '#22C55E',
          warning: '#F59E0B',
        },
        'dark-mode': {
          background: '#020617',
          card: '#0F172A',
          primary: '#3B82F6',
          'primary-foreground': '#020617',
          'text-primary': '#E5E7EB',
          'text-muted': '#94A3B8',
          border: '#1E293B',
          success: '#22C55E',
          warning: '#F59E0B',
        },
        // Define semantic colors as simple values
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        success: {
          DEFAULT: 'hsl(var(--success))',
          foreground: 'hsl(var(--success-foreground))',
        },
        warning: {
          DEFAULT: 'hsl(var(--warning))',
          foreground: 'hsl(var(--warning-foreground))',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif'],
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        DEFAULT: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out forwards',
        'slide-up': 'slideUp 0.3s ease-out forwards',
        'slide-down': 'slideDown 0.3s ease-out forwards',
        'bounce-slow': 'bounce 3s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        bounce: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    // Plugin to add the semantic color utilities
    plugin(function({ addUtilities }) {
      const newUtilities = {
        '.bg-background': {
          backgroundColor: 'hsl(var(--background))',
        },
        '.text-foreground': {
          color: 'hsl(var(--foreground))',
        },
        '.border-border': {
          borderColor: 'hsl(var(--border))',
        },
        '.bg-muted': {
          backgroundColor: 'hsl(var(--muted))',
        },
        '.text-muted-foreground': {
          color: 'hsl(var(--muted-foreground))',
        },
        '.bg-muted-foreground\\/30': {
          backgroundColor: 'hsl(var(--muted-foreground) / 0.3)',
        },
        '.bg-muted-foreground\\/50': {
          backgroundColor: 'hsl(var(--muted-foreground) / 0.5)',
        },
        '.text-primary-foreground': {
          color: 'hsl(var(--primary-foreground))',
        },
        '.text-secondary-foreground': {
          color: 'hsl(var(--secondary-foreground))',
        },
        '.text-destructive-foreground': {
          color: 'hsl(var(--destructive-foreground))',
        },
        '.text-accent-foreground': {
          color: 'hsl(var(--accent-foreground))',
        },
        '.text-popover-foreground': {
          color: 'hsl(var(--popover-foreground))',
        },
        '.text-card-foreground': {
          color: 'hsl(var(--card-foreground))',
        },
      };
      addUtilities(newUtilities);
    }),
  ],
}