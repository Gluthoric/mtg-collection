import React, { useRef, useState } from 'react';
import { Upload, Camera, Loader } from 'lucide-react';
import { CardRecognitionService } from '../../services/cardRecognitionService';
import { MagicCard } from '../../types/card';

export function ScannerInterface() {
  const [preview, setPreview] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recognizedCards, setRecognizedCards] = useState<MagicCard[]>([]);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const processImage = async (file: File) => {
    try {
      setIsProcessing(true);
      setError(null);
      const cards = await CardRecognitionService.recognizeCard(file);
      setRecognizedCards(cards);
    } catch (err) {
      setError('Failed to recognize card. Please try again.');
      console.error('Error processing image:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      processImage(file);
    }
  };

  const handleCameraCapture = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    } catch (err) {
      setError('Failed to access camera. Please check permissions.');
      console.error('Error accessing camera:', err);
    }
  };

  const captureFrame = () => {
    if (videoRef.current) {
      const canvas = document.createElement('canvas');
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0);
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
            setPreview(URL.createObjectURL(blob));
            processImage(file);
          }
        }, 'image/jpeg');
      }
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="space-y-4">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="flex justify-center">
            {isProcessing ? (
              <div className="flex flex-col items-center">
                <Loader className="w-12 h-12 animate-spin text-blue-600" />
                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  Processing image...
                </p>
              </div>
            ) : preview ? (
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
              disabled={isProcessing}
            >
              <Upload className="w-5 h-5" />
              Upload Image
            </button>

            <button
              onClick={handleCameraCapture}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              disabled={isProcessing}
            >
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

          <video
            ref={videoRef}
            className="hidden"
            onClick={captureFrame}
          />

          {recognizedCards.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-4">Recognized Cards</h3>
              <div className="space-y-4">
                {recognizedCards.map((card, index) => (
                  <div
                    key={`${card.id}-${index}`}
                    className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg"
                  >
                    <div className="flex items-start gap-4">
                      {card.image_uris?.small && (
                        <img
                          src={card.image_uris.small}
                          alt={card.name}
                          className="w-24 h-auto rounded"
                        />
                      )}
                      <div>
                        <h4 className="font-semibold">{card.name}</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {card.setName} ({card.set.toUpperCase()})
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          #{card.collector_number} · {card.rarity}
                        </p>
                        {card.prices?.usd && (
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            ${card.prices.usd}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
