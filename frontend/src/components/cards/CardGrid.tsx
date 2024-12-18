import React from 'react';
import type { MagicCard } from '../../types/card';

interface CardGridProps {
  cards: MagicCard[];
  onCardClick: (card: MagicCard) => void;
}

export function CardGrid({ cards, onCardClick }: CardGridProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-4">
      {cards.map((card) => (
        <div
          key={card.id}
          className="relative group cursor-pointer hover:transform hover:scale-105 transition-transform duration-200"
          onClick={() => onCardClick(card)}
        >
          <div className="rounded-lg overflow-hidden shadow-lg bg-white dark:bg-gray-800">
            <img
              src={card.image_uris?.normal}
              alt={card.name}
              className="w-full h-auto object-cover"
              loading="lazy"
            />
            <div className="p-3">
              <h3 className="font-medium text-gray-900 dark:text-gray-100">{card.name}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {card.set} · #{card.collector_number}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}