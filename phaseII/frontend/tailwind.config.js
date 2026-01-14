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
        // Soft, muted color palette for professional appearance
        primary: {
          50: 'hsl(220, 28%, 95%)',
          100: 'hsl(220, 28%, 88%)',
          200: 'hsl(220, 28%, 78%)',
          300: 'hsl(220, 28%, 68%)',
          400: 'hsl(220, 30%, 58%)',
          500: 'hsl(220, 30%, 52%)',  // Base - soft blue
          600: 'hsl(220, 32%, 42%)',  // Hover - slightly darker
          700: 'hsl(220, 34%, 32%)',  // Active
          800: 'hsl(220, 36%, 25%)',
          900: 'hsl(220, 38%, 18%)',
        },
        secondary: {
          50: 'hsl(200, 25%, 95%)',
          100: 'hsl(200, 25%, 88%)',
          200: 'hsl(200, 25%, 78%)',
          300: 'hsl(200, 25%, 68%)',
          400: 'hsl(200, 28%, 58%)',
          500: 'hsl(200, 28%, 52%)',  // Soft cyan
          600: 'hsl(200, 30%, 42%)',
          700: 'hsl(200, 32%, 32%)',
          800: 'hsl(200, 34%, 25%)',
          900: 'hsl(200, 36%, 18%)',
        },
        success: {
          50: 'hsl(145, 30%, 95%)',
          100: 'hsl(145, 30%, 88%)',
          200: 'hsl(145, 30%, 78%)',
          300: 'hsl(145, 30%, 68%)',
          400: 'hsl(145, 32%, 58%)',
          500: 'hsl(145, 32%, 48%)',  // Soft green
          600: 'hsl(145, 35%, 38%)',
          700: 'hsl(145, 38%, 30%)',
          800: 'hsl(145, 40%, 24%)',
          900: 'hsl(145, 42%, 18%)',
        },
        error: {
          50: 'hsl(0, 30%, 95%)',
          100: 'hsl(0, 30%, 88%)',
          200: 'hsl(0, 30%, 78%)',
          300: 'hsl(0, 30%, 68%)',
          400: 'hsl(0, 32%, 58%)',
          500: 'hsl(0, 32%, 52%)',  // Soft red
          600: 'hsl(0, 35%, 45%)',
          700: 'hsl(0, 38%, 38%)',
          800: 'hsl(0, 40%, 30%)',
          900: 'hsl(0, 42%, 22%)',
        },
        warning: {
          50: 'hsl(35, 30%, 95%)',
          100: 'hsl(35, 30%, 88%)',
          200: 'hsl(35, 30%, 78%)',
          300: 'hsl(35, 30%, 68%)',
          400: 'hsl(35, 32%, 58%)',
          500: 'hsl(35, 32%, 52%)',  // Soft orange
          600: 'hsl(35, 35%, 45%)',
          700: 'hsl(35, 38%, 38%)',
          800: 'hsl(35, 40%, 30%)',
          900: 'hsl(35, 42%, 22%)',
        },
        info: {
          50: 'hsl(210, 28%, 95%)',
          100: 'hsl(210, 28%, 88%)',
          200: 'hsl(210, 28%, 78%)',
          300: 'hsl(210, 28%, 68%)',
          400: 'hsl(210, 30%, 58%)',
          500: 'hsl(210, 30%, 52%)',  // Soft blue-gray
          600: 'hsl(210, 32%, 42%)',
          700: 'hsl(210, 34%, 32%)',
          800: 'hsl(210, 36%, 25%)',
          900: 'hsl(210, 38%, 18%)',
        },
        neutral: {
          50: 'hsl(210, 10%, 98%)',
          100: 'hsl(210, 10%, 95%)',
          200: 'hsl(210, 10%, 88%)',
          300: 'hsl(210, 10%, 78%)',
          400: 'hsl(210, 10%, 65%)',
          500: 'hsl(210, 10%, 55%)',  // Soft slate
          600: 'hsl(210, 12%, 42%)',
          700: 'hsl(210, 14%, 32%)',
          800: 'hsl(210, 16%, 22%)',
          900: 'hsl(210, 18%, 15%)',
        },
        // Define semantic colors as simple values
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
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