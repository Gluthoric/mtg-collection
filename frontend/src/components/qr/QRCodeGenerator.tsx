import React, { useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { Download } from 'lucide-react';

interface QRCodeGeneratorProps {
  collectionId: string;
  collectionName: string;
}

export function QRCodeGenerator({ collectionId, collectionName }: QRCodeGeneratorProps) {
  const [size, setSize] = useState(256);
  const qrValue = `mtg://collection/${collectionId}`;

  const downloadQR = () => {
    const svg = document.getElementById('qr-code');
    if (svg) {
      const svgData = new XMLSerializer().serializeToString(svg);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.onload = () => {
        canvas.width = size;
        canvas.height = size;
        ctx?.drawImage(img, 0, 0);
        const pngFile = canvas.toDataURL('image/png');
        const downloadLink = document.createElement('a');
        downloadLink.download = `${collectionName}-qr.png`;
        downloadLink.href = pngFile;
        downloadLink.click();
      };
      img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-center">{collectionName}</h2>
          
          <div className="flex justify-center">
            <div className="p-4 bg-white rounded-lg">
              <QRCodeSVG
                id="qr-code"
                value={qrValue}
                size={size}
                level="H"
                includeMargin={true}
              />
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">QR Code Size</label>
              <input
                type="range"
                min="128"
                max="512"
                step="32"
                value={size}
                onChange={(e) => setSize(Number(e.target.value))}
                className="w-full"
              />
            </div>

            <button
              onClick={downloadQR}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Download className="w-5 h-5" />
              Download QR Code
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}