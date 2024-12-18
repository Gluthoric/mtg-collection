import { MagicCard } from '../types/card';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export class CollectionAPI {
  private static statsCache: any = null;
  private static statsCacheTime: number = 0;
  private static statsPromise: Promise<any> | null = null;
  private static readonly CACHE_DURATION = 5000; // 5 seconds cache

  static async getStats() {
    try {
      // Check cache first
      const now = Date.now();
      if (this.statsCache && (now - this.statsCacheTime) < this.CACHE_DURATION) {
        console.log('Returning cached stats');
        return this.statsCache;
      }

      // If there's already a request in flight, return that promise
      if (this.statsPromise) {
        console.log('Returning in-flight stats request');
        return this.statsPromise;
      }

      console.log('Fetching fresh stats from:', `${API_BASE_URL}/api/stats`);
      const response = await fetch(`${API_BASE_URL}/api/stats`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Origin': 'http://localhost:5173'
        },
        mode: 'cors',
        cache: 'default' // Let browser handle caching
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      // Create new request promise
      this.statsPromise = response.json().then(data => {
        console.log('Received stats data:', data);
        // Update cache
        this.statsCache = data;
        this.statsCacheTime = now;
        // Clear promise
        this.statsPromise = null;
        return data;
      });
      
      return this.statsPromise;
    } catch (error) {
      console.error('Error fetching stats:', error);
      if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
        throw new Error('Unable to connect to the server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  private static setsCache: any = null;
  private static setsCacheTime: number = 0;
  private static setsPromise: Promise<any> | null = null;

  static async getSets() {
    try {
      // Check cache first
      const now = Date.now();
      if (this.setsCache && (now - this.setsCacheTime) < this.CACHE_DURATION) {
        console.log('Returning cached sets');
        return this.setsCache;
      }

      // If there's already a request in flight, return that promise
      if (this.setsPromise) {
        console.log('Returning in-flight sets request');
        return this.setsPromise;
      }

      const response = await fetch(`${API_BASE_URL}/api/sets`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Origin': window.location.origin
        },
        cache: 'default',
        mode: 'cors'
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      // Create new request promise
      this.setsPromise = response.json().then(data => {
        // Update cache
        this.setsCache = data;
        this.setsCacheTime = now;
        // Clear promise
        this.setsPromise = null;
        return data;
      });
      
      return this.setsPromise;
    } catch (error) {
      console.error('Error fetching sets:', error);
      throw new Error('Failed to fetch sets data. Please check your connection and try again.');
    }
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
