import React from 'react';
import { Settings } from '../settings/Settings';

export function SettingsView() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      <Settings />
    </div>
  );
}