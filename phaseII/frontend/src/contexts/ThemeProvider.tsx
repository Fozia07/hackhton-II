'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

/**
 * ThemeProvider with SaaS-style theme colors
 * Provides smooth transitions between light and dark themes with specified color scheme
 */
export function ThemeProvider({
  children,
  defaultTheme = 'light',
  storageKey = 'theme'
}: {
  children: ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
}) {
  const [theme, setThemeState] = useState<Theme>('light'); // Default to 'light' initially
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Only run on client side
    if (typeof window !== 'undefined') {
      // Get theme from localStorage or use default
      const storedTheme = localStorage.getItem(storageKey) as Theme | null;
      const initialTheme = storedTheme || defaultTheme;
      setThemeState(initialTheme);

      // Apply the theme class immediately to avoid FOUC
      const root = window.document.documentElement;
      root.classList.remove('light', 'dark');
      root.classList.add(initialTheme);
    }
    setMounted(true);
  }, [storageKey, defaultTheme]);

  useEffect(() => {
    if (!mounted || typeof window === 'undefined') return;

    const root = window.document.documentElement;

    // Remove old theme classes
    root.classList.remove('light', 'dark');

    // Add new theme class
    root.classList.add(theme);

    // Set CSS custom properties based on theme with specified SaaS colors
    if (theme === 'light') {
      root.style.setProperty('--background', '#CFE8FA');
      root.style.setProperty('--card', '#FFFFFF');
      root.style.setProperty('--primary', '#2563EB');
      root.style.setProperty('--primary-foreground', '#CFE8FA');
      root.style.setProperty('--text-primary', '#0F172A');
      root.style.setProperty('--text-muted', '#64748B');
      root.style.setProperty('--border', '#E2E8F0');
      root.style.setProperty('--success', '#22C55E');
      root.style.setProperty('--warning', '#F59E0B');
    } else {
      root.style.setProperty('--background', '#0F172A');
      root.style.setProperty('--card', '#0F172A');
      root.style.setProperty('--primary', '#3B82F6');
      root.style.setProperty('--primary-foreground', '#0F172A');
      root.style.setProperty('--text-primary', '#E5E7EB');
      root.style.setProperty('--text-muted', '#94A3B8');
      root.style.setProperty('--border', '#1E293B');
      root.style.setProperty('--success', '#22C55E');
      root.style.setProperty('--warning', '#F59E0B');
    }

    // Add smooth transition for theme switching
    root.style.setProperty('transition', 'background-color 0.3s ease, color 0.3s ease');

    // Save to localStorage
    localStorage.setItem(storageKey, theme);

    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute(
        'content',
        theme === 'dark' ? '#0F172A' : '#CFE8FA'
      );
    }

    // Clean up transition after theme change completes
    const timeoutId = setTimeout(() => {
      root.style.removeProperty('transition');
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [theme, mounted]);

  const setTheme = (theme: Theme) => {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      setThemeState(theme);
      localStorage.setItem(storageKey, theme);
    }
  };

  const toggleTheme = () => {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      setThemeState(prev => {
        const newTheme = prev === 'light' ? 'dark' : 'light';
        localStorage.setItem(storageKey, newTheme);
        return newTheme;
      });
    }
  };

  // Prevent flash of unstyled content
  if (!mounted) {
    return <>{children}</>;
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}