#!/usr/bin/env python3

import io
import os
import requests
import time
from google.cloud import vision

# Set up Google Cloud credentials with absolute path
credentials_path = '/home/gluth/mtg-collection/service_account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

print(f"Using credentials from: {credentials_path}")
if not os.path.exists(credentials_path):
    print(f"ERROR: Credentials file not found at {credentials_path}")
    exit(1)

class ScryfallAPI:
    """Handle Scryfall API interactions with rate limiting."""

    BASE_URL = "https://api.scryfall.com"

    @staticmethod
    def search_card(query):
        """Search for all printings of a card on Scryfall."""
        try:
            # Add a small delay to respect rate limits
            time.sleep(0.1)

            # First try exact match
            print(f"Querying Scryfall API with exact match: {query}")
            response = requests.get(
                f"{ScryfallAPI.BASE_URL}/cards/search",
                params={
                    "q": f"!\"{query}\"",
                    "order": "released",
                    "unique": "prints"  # Get all printings
                }
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    return data['data']

            # If exact match fails, try fuzzy search
            if response.status_code == 404:
                print("No exact matches found, trying fuzzy search...")
                response = requests.get(
                    f"{ScryfallAPI.BASE_URL}/cards/search",
                    params={
                        "q": query,
                        "order": "released",
                        "unique": "prints"  # Get all printings
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('data'):
                        return data['data']

            return None

        except requests.exceptions.RequestException as e:
            print(f"Error querying Scryfall API: {e}")
            return None

def detect_text(image_path):
    """Detects text in an image using Google Vision API."""
    try:
        print(f"Initializing Vision API client...")
        client = vision.ImageAnnotatorClient()

        if not os.path.exists(image_path):
            print(f"ERROR: Image file not found at {image_path}")
            return None

        print(f"Reading image file...")
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        print(f"Creating image object...")
        image = vision.Image(content=content)

        print(f"Sending request to Vision API...")
        response = client.text_detection(image=image)

        if response.error.message:
            print(f"Error from Vision API: {response.error.message}")
            return None

        print(f"Processing Vision API response...")
        texts = response.text_annotations

        if not texts:
            print("No text annotations found in the response")
            return None

        print(f"Found {len(texts)} text annotations")
        # Print first annotation which contains all text
        print(f"Full text: {texts[0].description}")

        return texts[0].description if texts else None

    except Exception as e:
        print(f"Unexpected error in detect_text: {str(e)}")
        return None

def extract_card_name(text):
    """Extract card name from the detected text."""
    if not text:
        return None

    # Split into lines and take the first line as the card name
    lines = text.split('\n')
    print(f"First few lines of text: {lines[:3]}")

    card_name = lines[0].strip()
    print(f"Extracted card name: {card_name}")

    return card_name

def process_image(image_path):
    """Processes an image to identify the Magic card."""
    print(f"\nProcessing image: {image_path}")

    detected_text = detect_text(image_path)
    if detected_text:
        print(f"\nDetected raw text: {detected_text}")

        card_name = extract_card_name(detected_text)
        if card_name:
            print(f"\nSearching Scryfall for all printings of: {card_name}")
            printings = ScryfallAPI.search_card(card_name)
            if printings:
                print(f"\nFound {len(printings)} printings:")
                print("\n=== Card Printings ===")
                for i, card in enumerate(printings, 1):
                    print(f"\nPrinting {i}:")
                    print(f"Set: {card['set_name']} ({card['set'].upper()})")
                    print(f"Released: {card.get('released_at', 'N/A')}")
                    print(f"Rarity: {card['rarity']}")
                    if 'image_uris' in card:
                        print(f"Image URL: {card['image_uris']['normal']}")
                    print(f"Collector Number: {card.get('collector_number', 'N/A')}")

                # Print detailed card information using the first printing
                print("\n=== Card Details ===")
                print(f"Name: {printings[0]['name']}")
                print(f"Mana Cost: {printings[0].get('mana_cost', 'N/A')}")
                print(f"Type Line: {printings[0].get('type_line', 'N/A')}")
                print(f"Oracle Text: {printings[0].get('oracle_text', 'N/A')}")
            else:
                print("Card not found in Scryfall database")
        else:
            print("Failed to extract card name")
    else:
        print("No text detected in the image")

if __name__ == "__main__":
    test_image = input("Enter path to card image: ")
    process_image(test_image)
