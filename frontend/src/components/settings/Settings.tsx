import React from 'react';
import { ThemeSettings } from './ThemeSettings';
import { NotificationSettings } from './NotificationSettings';

export function Settings() {
  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <ThemeSettings />
      <NotificationSettings />
    </div>
  );
}