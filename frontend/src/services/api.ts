import { MagicCard } from '../types/card';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export class CollectionAPI {
  static async getStats() {
    const response = await fetch(`${API_BASE_URL}/api/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }

  static async getSets() {
    const response = await fetch(`${API_BASE_URL}/api/sets`);
    if (!response.ok) throw new Error('Failed to fetch sets');
    return response.json();
  }

  static async getSetCards(setName: string) {
    const response = await fetch(`${API_BASE_URL}/api/set/${encodeURIComponent(setName)}/cards`);
    if (!response.ok) throw new Error('Failed to fetch set cards');
    return response.json();
  }

  static async updateCard(scryfallId: string, quantities: { quantity: number; foil_quantity: number }) {
    const response = await fetch(`${API_BASE_URL}/api/card/${scryfallId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(quantities),
    });
    if (!response.ok) throw new Error('Failed to update card');
    return response.json();
  }
}