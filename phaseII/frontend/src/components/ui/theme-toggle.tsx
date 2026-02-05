import { Moon, Sun } from 'lucide-react';

import { useTheme } from '@/contexts/ThemeProvider';
import { Button } from '@/components/ui/button';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      aria-label="Toggle theme"
      className="rounded-full hover:bg-muted focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
    >
      <Sun
        className={`h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0 ${
          theme === 'dark' ? 'text-muted-foreground' : ''
        }`}
        aria-hidden="true"
      />
      <Moon
        className={`absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100 ${
          theme === 'light' ? 'text-muted-foreground' : ''
        }`}
        aria-hidden="true"
      />
    </Button>
  );
}