import React from 'react';
import type { MagicCard } from '../../types/card';
import { X } from 'lucide-react';

interface CardDetailProps {
  card: MagicCard;
  onClose: () => void;
}

export function CardDetail({ card, onClose }: CardDetailProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h2 className="text-xl font-bold">{card.name}</h2>
          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <div className="p-4 flex flex-col md:flex-row gap-6">
          <div className="md:w-1/2">
            <img
              src={card.image_uris?.large}
              alt={card.name}
              className="rounded-lg w-full"
            />
          </div>
          
          <div className="md:w-1/2 space-y-4">
            <div>
              <h3 className="font-semibold text-lg">Card Information</h3>
              <p className="text-gray-600 dark:text-gray-400">{card.type_line}</p>
              {card.oracle_text && (
                <p className="mt-2 whitespace-pre-line">{card.oracle_text}</p>
              )}
            </div>
            
            <div>
              <h3 className="font-semibold text-lg">Set Details</h3>
              <p>
                {card.setName} ({card.set}) · #{card.collector_number}
              </p>
              <p className="capitalize">{card.rarity}</p>
            </div>
            
            {card.prices && (
              <div>
                <h3 className="font-semibold text-lg">Market Prices</h3>
                <p>Regular: ${card.prices.usd || 'N/A'}</p>
                <p>Foil: ${card.prices.usd_foil || 'N/A'}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}