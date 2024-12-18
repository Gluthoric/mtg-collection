export interface MagicCard {
  id: string;
  name: string;
  set: string;
  setName: string;
  collector_number: string;
  image_uris?: {
    small: string;
    normal: string;
    large: string;
  };
  mana_cost?: string;
  type_line: string;
  oracle_text?: string;
  colors: string[];
  rarity: string;
  prices?: {
    usd?: string;
    usd_foil?: string;
  };
}

export interface CollectionStats {
  totalCards: number;
  uniqueCards: number;
  totalValue: number;
  cardsByColor: Record<string, number>;
  cardsByRarity: Record<string, number>;
}