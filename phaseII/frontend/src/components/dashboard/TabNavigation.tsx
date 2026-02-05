'use client';

import React, { useState } from 'react';
import { Tabs, TabList, TabButton } from '@/components/ui/Tab';

interface TabNavigationProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const TabNavigation: React.FC<TabNavigationProps> = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'all', label: 'All' },
    { id: 'active', label: 'Active' },
    { id: 'completed', label: 'Completed' },
  ];

  return (
    <Tabs className="w-full">
      <TabList>
        {tabs.map((tab) => (
          <TabButton
            key={tab.id}
            id={tab.id}
            selected={activeTab === tab.id}
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
          </TabButton>
        ))}
      </TabList>
    </Tabs>
  );
};

export { TabNavigation };