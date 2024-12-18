import React from 'react';
import { Library, TrendingUp, DollarSign } from 'lucide-react';

interface SetData {
  set_name: string;
  total_possible: number;
  owned_cards: number;
  total_copies: number;
  total_value: number;
}

interface SetListProps {
  sets: SetData[];
  onSetClick: (setName: string) => void;
}

export function SetList({ sets, onSetClick }: SetListProps) {
  return (
    <div className="grid gap-4 p-4">
      {sets.map((set) => (
        <div
          key={set.set_name}
          onClick={() => onSetClick(set.set_name)}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 cursor-pointer 
                     hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold mb-2">{set.set_name}</h3>
              <div className="flex gap-6">
                <div className="flex items-center gap-2">
                  <Library className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {set.owned_cards}/{set.total_possible} cards
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-green-600 dark:text-green-400" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {((set.owned_cards / set.total_possible) * 100).toFixed(1)}% complete
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-yellow-600 dark:text-yellow-400" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    ${set.total_value.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
