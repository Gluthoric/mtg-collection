import React from 'react';
import { QRCodeGenerator } from '../qr/QRCodeGenerator';

export function QRView() {
  // Mock collection data
  const mockCollection = {
    id: '123456',
    name: 'My MTG Collection'
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">QR Code Generator</h1>
      <QRCodeGenerator
        collectionId={mockCollection.id}
        collectionName={mockCollection.name}
      />
    </div>
  );
}