import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';

export function ThemeSettings() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Theme Settings</h2>
      <div className="flex items-center gap-4">
        <button
          onClick={() => setTheme('light')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
            theme === 'light'
              ? 'bg-blue-100 text-blue-600'
              : 'hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <Sun className="w-5 h-5" />
          Light
        </button>
        <button
          onClick={() => setTheme('dark')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
            theme === 'dark'
              ? 'bg-blue-100 text-blue-600'
              : 'hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <Moon className="w-5 h-5" />
          Dark
        </button>
      </div>
    </div>
  );
}