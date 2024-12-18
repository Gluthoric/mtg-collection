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
  onSortChange: (sort: string) => void;
  onFilterChange: (filter: string) => void;
  currentSort: string;
  currentFilter: string;
}

export function SetList({ sets, onSetClick, onSortChange, onFilterChange, currentSort, currentFilter }: SetListProps) {
  return (
    <div className="space-y-4 p-4">
      <div className="flex gap-4 bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium">Sort by:</label>
          <select 
            value={currentSort}
            onChange={(e) => onSortChange(e.target.value)}
            className="rounded border dark:bg-gray-700 dark:border-gray-600 px-2 py-1"
          >
            <option value="name">Name</option>
            <option value="completion">Completion</option>
            <option value="value">Value</option>
            <option value="cards">Cards</option>
          </select>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium">Filter:</label>
          <select
            value={currentFilter}
            onChange={(e) => onFilterChange(e.target.value)}
            className="rounded border dark:bg-gray-700 dark:border-gray-600 px-2 py-1"
          >
            <option value="all">All Sets</option>
            <option value="incomplete">Incomplete</option>
            <option value="complete">Complete</option>
            <option value="empty">Empty</option>
          </select>
        </div>
      </div>
      <div className="grid gap-4">
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
  </div>
  );
}
