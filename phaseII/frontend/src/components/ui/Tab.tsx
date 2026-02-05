'use client';

import React, { useState } from 'react';
import { cn } from '@/lib/utils';

interface TabProps {
  children: React.ReactNode;
  className?: string;
}

interface TabListProps {
  children: React.ReactNode;
  className?: string;
}

interface TabPanelProps {
  children: React.ReactNode;
  id: string;
  className?: string;
  selected?: boolean;
}

interface TabButtonProps {
  children: React.ReactNode;
  id: string;
  selected?: boolean;
  onClick: () => void;
  className?: string;
}

const Tabs = ({ children, className }: TabProps) => {
  return (
    <div className={cn('flex flex-col', className)}>
      {children}
    </div>
  );
};

const TabList = ({ children, className }: TabListProps) => {
  return (
    <div
      role="tablist"
      className={cn(
        'flex border-b border-gray-200 dark:border-gray-700',
        className
      )}
    >
      {children}
    </div>
  );
};

const TabButton = ({
  children,
  id,
  selected,
  onClick,
  className
}: TabButtonProps) => {
  return (
    <button
      role="tab"
      aria-selected={selected}
      aria-controls={`${id}-panel`}
      id={id}
      onClick={onClick}
      className={cn(
        'px-4 py-2 text-sm font-medium rounded-t-lg transition-colors duration-200',
        selected
          ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-blue-900/20 dark:text-blue-400'
          : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:bg-gray-800',
        className
      )}
    >
      {children}
    </button>
  );
};

const TabPanel = ({
  children,
  id,
  selected,
  className
}: TabPanelProps) => {
  if (!selected) {
    return null;
  }

  return (
    <div
      role="tabpanel"
      id={`${id}-panel`}
      aria-labelledby={id}
      hidden={!selected}
      className={cn(
        'mt-4 p-4 rounded-lg bg-white dark:bg-gray-800 shadow-sm',
        className
      )}
    >
      {children}
    </div>
  );
};

export { Tabs, TabList, TabButton, TabPanel };