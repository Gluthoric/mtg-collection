import React from 'react';
import { NavLink } from 'react-router-dom';
import { Library, ScanLine, QrCode, Settings } from 'lucide-react';

const navItems = [
  { icon: Library, label: 'Collection', path: '/' },
  { icon: ScanLine, label: 'Scanner', path: '/scanner' },
  { icon: QrCode, label: 'QR Codes', path: '/qr' },
  { icon: Settings, label: 'Settings', path: '/settings' },
];

export function Sidebar() {
  return (
    <aside className="bg-white dark:bg-gray-800 w-64 min-h-screen p-4 border-r border-gray-200 dark:border-gray-700">
      <div className="flex items-center gap-2 mb-8 px-2">
        <Library className="w-8 h-8 text-blue-600" />
        <h1 className="text-xl font-bold">MTG Manager</h1>
      </div>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}