import React, { useRef, useState } from 'react';
import { Upload, Camera } from 'lucide-react';

export function ScannerInterface() {
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="space-y-4">
          <div className="flex justify-center">
            {preview ? (
              <img
                src={preview}
                alt="Card preview"
                className="max-w-full h-auto rounded-lg"
              />
            ) : (
              <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-12 text-center">
                <Upload className="mx-auto w-12 h-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  Upload a card image or use camera
                </p>
              </div>
            )}
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Upload className="w-5 h-5" />
              Upload Image
            </button>
            
            <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
              <Camera className="w-5 h-5" />
              Use Camera
            </button>
          </div>

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            className="hidden"
          />
        </div>
      </div>
    </div>
  );
}