import React from 'react';
import type { CollectionStats as Stats } from '../../types/card';
import { Library, Palette, Star, DollarSign } from 'lucide-react';

interface CollectionStatsProps {
  stats: Stats;
}

export function CollectionStats({ stats }: CollectionStatsProps) {
  console.log('CollectionStats received stats:', stats);
  
  // Ensure stats is not undefined before using it
  if (!stats) {
    console.warn('Stats object is undefined');
    return <div>Loading stats...</div>;
  }

  const statCards = [
    {
      icon: Library,
      label: 'Total Cards',
      value: stats.total_cards.toLocaleString(),
    },
    {
      icon: Star,
      label: 'Unique Cards',
      value: stats.unique_cards.toLocaleString(),
    },
    {
      icon: DollarSign,
      label: 'Total Value',
      value: `$${stats.total_value.toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}`,
    },
    {
      icon: Palette,
      label: 'Collection Progress',
      value: `${((stats.unique_cards / stats.total_possible) * 100).toFixed(1)}%`,
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
      {statCards.map((stat) => (
        <div
          key={stat.label}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6"
        >
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
              <stat.icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</p>
              <p className="text-2xl font-bold">{stat.value}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
