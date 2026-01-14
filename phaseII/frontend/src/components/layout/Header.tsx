// Enhanced Header Component with Soft Colors and Obvious Hover Effects
'use client';

import React from 'react';
import Link from 'next/link';
import { useTheme } from '@/contexts/ThemeProvider';
import { Button } from '@/components/ui/button';
import { Sun, Moon, Menu } from 'lucide-react';
import { motion } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

export const Header = () => {
  const { theme, toggleTheme } = useTheme();
  const reducedMotion = useReducedMotion();

  return (
    <header className='sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur-md supports-[backdrop-filter]:bg-background/80 shadow-[var(--shadow-sm)] transition-all duration-250'>
      <div className='container flex h-16 items-center justify-between px-4'>
        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, x: -20 }}
          animate={reducedMotion ? {} : { opacity: 1, x: 0 }}
          transition={reducedMotion ? {} : { duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          className='flex items-center gap-2'
        >
          <Link href='/' className='flex items-center space-x-3 group'>
            <motion.div
              whileHover={reducedMotion ? {} : { scale: 1.05, rotate: 5 }}
              whileTap={reducedMotion ? {} : { scale: 0.95 }}
              className='h-9 w-9 rounded-full bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-600 dark:from-primary-400 dark:via-primary-500 dark:to-secondary-500 shadow-[var(--shadow-sm)] group-hover:shadow-[var(--shadow-md)] transition-shadow duration-200'
            ></motion.div>
            <span className='text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-400 dark:to-secondary-400'>
              TodoApp
            </span>
          </Link>
        </motion.div>

        <nav className='hidden md:flex items-center space-x-2 text-sm font-medium'>
          <motion.div whileHover={reducedMotion ? {} : { scale: 1.05 }} whileTap={reducedMotion ? {} : { scale: 0.95 }}>
            <Link
              href='/'
              className='px-4 py-2 rounded-md transition-all duration-200 text-muted-foreground hover:text-foreground hover:bg-primary-50 dark:hover:bg-primary-900/20 hover:shadow-[var(--shadow-sm)]'
            >
              Home
            </Link>
          </motion.div>
          <motion.div whileHover={reducedMotion ? {} : { scale: 1.05 }} whileTap={reducedMotion ? {} : { scale: 0.95 }}>
            <Link
              href='/dashboard'
              className='px-4 py-2 rounded-md transition-all duration-200 text-muted-foreground hover:text-foreground hover:bg-primary-50 dark:hover:bg-primary-900/20 hover:shadow-[var(--shadow-sm)]'
            >
              Dashboard
            </Link>
          </motion.div>
        </nav>

        <div className='flex items-center gap-2'>
          <motion.div whileHover={reducedMotion ? {} : { scale: 1.1 }} whileTap={reducedMotion ? {} : { scale: 0.95 }}>
            <Button
              variant='ghost'
              size='icon'
              onClick={toggleTheme}
              aria-label='Toggle theme'
              className='h-10 w-10 rounded-full border-2 border-transparent hover:border-primary-200 dark:hover:border-primary-700 hover:bg-primary-50 dark:hover:bg-primary-900/20 hover:shadow-[var(--shadow-sm)] transition-all duration-200'
            >
              {theme === 'dark' ? (
                <Sun className='h-5 w-5 text-warning-500 dark:text-warning-400' />
              ) : (
                <Moon className='h-5 w-5 text-primary-600 dark:text-primary-400' />
              )}
            </Button>
          </motion.div>

          <Button asChild className='hidden md:block'>
            <Link href='/dashboard'>Dashboard</Link>
          </Button>

          <motion.div whileHover={reducedMotion ? {} : { scale: 1.1 }} whileTap={reducedMotion ? {} : { scale: 0.95 }}>
            <Button
              variant='ghost'
              size='icon'
              className='md:hidden h-10 w-10 rounded-full hover:bg-primary-50 dark:hover:bg-primary-900/20 hover:shadow-[var(--shadow-sm)]'
            >
              <Menu className='h-5 w-5' />
            </Button>
          </motion.div>
        </div>
      </div>
    </header>
  );
};
