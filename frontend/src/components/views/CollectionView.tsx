import React, { useState } from 'react';
import { CardGrid } from '../cards/CardGrid';
import { CardDetail } from '../cards/CardDetail';
import { CollectionStats } from '../stats/CollectionStats';
import type { MagicCard } from '../../types/card';

export function CollectionView() {
  const [selectedCard, setSelectedCard] = useState<MagicCard | null>(null);

  // Mock data for demonstration
  const mockStats = {
    totalCards: 1234,
    uniqueCards: 789,
    totalValue: 2500.50,
    cardsByColor: { Blue: 300, Red: 250, Green: 200, White: 150, Black: 100 },
    cardsByRarity: { Common: 500, Uncommon: 300, Rare: 200, Mythic: 50 }
  };

  const mockCards: MagicCard[] = []; // Add mock cards here

  return (
    <div className="space-y-6">
      <CollectionStats stats={mockStats} />
      <CardGrid cards={mockCards} onCardClick={setSelectedCard} />
      {selectedCard && (
        <CardDetail card={selectedCard} onClose={() => setSelectedCard(null)} />
      )}
    </div>
  );
}