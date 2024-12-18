import React from 'react';
import { ScannerInterface } from '../scanner/ScannerInterface';

export function ScannerView() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Card Scanner</h1>
      <ScannerInterface />
    </div>
  );
}