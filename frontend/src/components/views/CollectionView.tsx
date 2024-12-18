import React, { useState, useEffect } from 'react';
import { CardGrid } from '../cards/CardGrid';
import { CardDetail } from '../cards/CardDetail';
import { CollectionStats } from '../stats/CollectionStats';
import { CollectionAPI } from '../../services/api';
import type { MagicCard, CollectionStats as Stats } from '../../types/card';

export function CollectionView() {
  const [selectedCard, setSelectedCard] = useState<MagicCard | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [cards, setCards] = useState<MagicCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function fetchData() {
      try {
        setLoading(true);
        setError(null);
        
        const [statsData, setsData] = await Promise.all([
          CollectionAPI.getStats(),
          CollectionAPI.getSets()
        ]);
        
        // Only update state if component is still mounted
        if (mounted) {
          setStats(statsData);
          // For now, we'll just get cards from the first set
          if (setsData.length > 0) {
            const firstSetCards = await CollectionAPI.getSetCards(setsData[0].set_name);
            setCards(firstSetCards);
          }
        }
      } catch (err) {
        console.error('Error fetching collection data:', err);
        if (mounted) {
          setError('Failed to load collection data. Please check your connection and try again.');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    fetchData();

    // Cleanup function to prevent state updates after unmount
    return () => {
      mounted = false;
    };
  }, []); // Empty dependency array means this effect runs once on mount

  if (loading) {
    return <div className="p-4">Loading collection data...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-600">{error}</div>;
  }

  return (
    <div className="space-y-6">
      {stats && <CollectionStats stats={stats} />}
      <CardGrid cards={cards} onCardClick={setSelectedCard} />
      {selectedCard && (
        <CardDetail card={selectedCard} onClose={() => setSelectedCard(null)} />
      )}
    </div>
  );
}
