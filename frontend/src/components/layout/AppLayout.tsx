import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CollectionView } from '../views/CollectionView';
import { ScannerView } from '../views/ScannerView';
import { QRView } from '../views/QRView';
import { SettingsView } from '../views/SettingsView';

export function AppLayout() {
  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<CollectionView />} />
            <Route path="/scanner" element={<ScannerView />} />
            <Route path="/qr" element={<QRView />} />
            <Route path="/settings" element={<SettingsView />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}