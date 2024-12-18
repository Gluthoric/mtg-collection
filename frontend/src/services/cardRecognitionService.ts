import { MagicCard } from '../types/card';

export class CardRecognitionService {
  private static readonly API_URL = '/api/card-recognition';  // Update with actual API endpoint

  static async recognizeCard(imageFile: File): Promise<MagicCard[]> {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await fetch(`${this.API_URL}/identify`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.printings;
    } catch (error) {
      console.error('Error recognizing card:', error);
      throw error;
    }
  }
}
