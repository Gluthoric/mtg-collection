import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Set

class CollectionTracker:
    def __init__(self):
        self.scryfall_cards: Dict[str, dict] = {}  # id -> card data
        self.collection: Dict[str, List[dict]] = {}  # id -> list of owned copies
        self.load_scryfall_data()
        self.load_collection()

    def load_scryfall_data(self):
        """Load Scryfall default cards data"""
        print("Loading Scryfall data...")
        with open('default-cards-20241216100811.json', 'r', encoding='utf-8') as f:
            cards = json.load(f)
            for card in cards:
                self.scryfall_cards[card['id']] = card
        print(f"Loaded {len(self.scryfall_cards)} cards from Scryfall")

    def load_collection(self):
        """Load collection data from CSV files"""
        print("Loading collection data...")
        collection_count = 0
        
        # Walk through organized_sets directory
        for root, _, files in os.walk('organized_sets'):
            for file in files:
                if file.endswith('_with_scryfall.csv'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            scryfall_id = row['scryfall_id']
                            if not scryfall_id:
                                continue
                                
                            if scryfall_id not in self.collection:
                                self.collection[scryfall_id] = []
                            
                            # Add this copy to collection
                            self.collection[scryfall_id].append({
                                'set': row['Set'],
                                'quantity': int(row['Qty']),
                                'foil': row['Foil'].upper() == 'TRUE',
                                'collector_number': row['collector_number']
                            })
                            collection_count += int(row['Qty'])

        print(f"Loaded {collection_count} cards across {len(self.collection)} unique cards")

    def get_collection_stats(self) -> dict:
        """Get statistics about the collection"""
        stats = {
            'total_cards': 0,
            'unique_cards': len(self.collection),
            'foil_cards': 0,
            'by_rarity': {'common': 0, 'uncommon': 0, 'rare': 0, 'mythic': 0},
            'by_set': {},
            'estimated_value': 0.0
        }

        for card_id, copies in self.collection.items():
            card_data = self.scryfall_cards.get(card_id)
            if not card_data:
                continue

            for copy in copies:
                qty = copy['quantity']
                stats['total_cards'] += qty
                
                if copy['foil']:
                    stats['foil_cards'] += qty

                # Track by set
                set_name = copy['set']
                if set_name not in stats['by_set']:
                    stats['by_set'][set_name] = 0
                stats['by_set'][set_name] += qty

                # Track by rarity
                rarity = card_data.get('rarity', 'unknown')
                if rarity in stats['by_rarity']:
                    stats['by_rarity'][rarity] += qty

                # Add value if available
                if 'prices' in card_data:
                    price_key = 'usd_foil' if copy['foil'] else 'usd'
                    if card_data['prices'].get(price_key):
                        stats['estimated_value'] += float(card_data['prices'][price_key]) * qty

        return stats

    def add_card(self, card_name: str, set_name: str, quantity: int = 1, foil: bool = False) -> bool:
        """Add a card to the collection"""
        # Find card in Scryfall data
        card_data = None
        card_id = None
        
        for id, data in self.scryfall_cards.items():
            if data['name'] == card_name and data.get('set_name', '').lower() == set_name.lower():
                card_data = data
                card_id = id
                break

        if not card_data:
            print(f"Could not find card: {card_name} from set: {set_name}")
            return False

        # Add to collection
        if card_id not in self.collection:
            self.collection[card_id] = []

        # Check if we already have this exact version
        for copy in self.collection[card_id]:
            if copy['set'] == set_name and copy['foil'] == foil:
                copy['quantity'] += quantity
                break
        else:
            # Add new copy
            self.collection[card_id].append({
                'set': set_name,
                'quantity': quantity,
                'foil': foil,
                'collector_number': card_data.get('collector_number', '')
            })

        return True

    def remove_card(self, card_name: str, set_name: str, quantity: int = 1, foil: bool = False) -> bool:
        """Remove a card from the collection"""
        # Find card in collection
        for card_id, copies in self.collection.items():
            card_data = self.scryfall_cards[card_id]
            if card_data['name'] == card_name:
                for copy in copies:
                    if copy['set'] == set_name and copy['foil'] == foil:
                        if copy['quantity'] <= quantity:
                            copies.remove(copy)
                            if not copies:
                                del self.collection[card_id]
                        else:
                            copy['quantity'] -= quantity
                        return True
        
        print(f"Could not find card to remove: {card_name} from set: {set_name}")
        return False

    def save_collection(self):
        """Save collection back to CSV files"""
        # Group cards by set
        sets: Dict[str, List[dict]] = {}
        
        for card_id, copies in self.collection.items():
            card_data = self.scryfall_cards[card_id]
            for copy in copies:
                set_name = copy['set']
                if set_name not in sets:
                    sets[set_name] = []
                
                sets[set_name].append({
                    'Name': card_data['name'],
                    'Set': copy['set'],
                    'Qty': copy['quantity'],
                    'Foil': str(copy['foil']).upper(),
                    'scryfall_id': card_id,
                    'collector_number': copy['collector_number'],
                    'scryfall_set': card_data.get('set', ''),
                    'scryfall_rarity': card_data.get('rarity', '')
                })

        # Save each set
        for set_name, cards in sets.items():
            # Determine set type (commander, core, masters, etc)
            set_type = 'standard'  # default
            set_lower = set_name.lower()
            if 'commander' in set_lower:
                set_type = 'commander'
            elif any(x in set_lower for x in ['masters', 'horizons']):
                set_type = 'masters'
            elif 'core' in set_lower or 'edition' in set_lower:
                set_type = 'core'
            elif any(x in set_lower for x in ['secret lair', 'universes', 'doctor who']):
                set_type = 'special'
            elif 'promo' in set_lower or 'buy-a-box' in set_lower:
                set_type = 'promo'

            # Create directory if needed
            dir_path = os.path.join('organized_sets', set_type)
            os.makedirs(dir_path, exist_ok=True)

            # Save to CSV
            filepath = os.path.join(dir_path, f"{set_name}_with_scryfall.csv")
            fieldnames = ['Name', 'Set', 'Qty', 'Foil', 'scryfall_id', 
                         'collector_number', 'scryfall_set', 'scryfall_rarity']
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sorted(cards, key=lambda x: int(x['collector_number']) if x['collector_number'].isdigit() else float('inf')))

if __name__ == '__main__':
    tracker = CollectionTracker()
    
    # Example usage:
    stats = tracker.get_collection_stats()
    print("\nCollection Statistics:")
    print(f"Total Cards: {stats['total_cards']}")
    print(f"Unique Cards: {stats['unique_cards']}")
    print(f"Foil Cards: {stats['foil_cards']}")
    print("\nBy Rarity:")
    for rarity, count in stats['by_rarity'].items():
        print(f"  {rarity.title()}: {count}")
    print(f"\nEstimated Value: ${stats['estimated_value']:.2f}")
