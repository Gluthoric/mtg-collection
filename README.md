# MTG Collection Manager

A comprehensive Magic: The Gathering collection management system with card recognition capabilities.

## Features

- Card recognition using Google Cloud Vision API
- Multiple services for different aspects of collection management
- Support for various card frames and sets
- Integration with Scryfall API for accurate card information
- Web interface for card scanning and collection management

## Project Structure

- `services/card-recognition/vision-api`: Card recognition service using Google Cloud Vision
- `services/collection-api`: API for managing collection data
- `services/mobile-scanner`: Mobile scanning capabilities
- `services/qr-service`: QR code generation and scanning
- `frontend`: Web and mobile client applications
  - `web-client`: React-based web interface
  - `mobile-app`: Mobile application components
- `database`: Database migrations and models
- `docs`: Project documentation
- `utils`: Utility scripts and tools

## Setup

1. Install dependencies:
```bash
# Backend dependencies
cd services/card-recognition/vision-api
python3 -m venv venv
source venv/bin/activate
pip install google-cloud-vision requests

# Frontend dependencies
cd frontend
npm install
```

2. Configure Google Cloud Vision API:
- Set up a Google Cloud project
- Enable the Vision API
- Create a service account and download credentials
- Save credentials as `service_account.json` in the project root

3. Start the development servers:

```bash
# Start the Vision API server (from project root)
cd services/card-recognition/vision-api
python3 card_identifier.py

# In a new terminal, start the frontend development server
cd frontend
npm run dev
```

## Usage

### Card Recognition Web Interface

1. Access the web interface at `http://localhost:5173` (or the URL shown in your terminal)
2. Use the card scanner interface to:
   - Upload card images from your device
   - Use your device's camera to capture card images
   - View recognized cards with their details from Scryfall
   - Add recognized cards to your collection

The card recognition service can identify Magic cards from images and retrieve detailed card information including all printings throughout Magic's history.

Example Python usage:
```python
python3 services/card-recognition/vision-api/card_identifier.py
# Enter the path to your card image when prompted
```

## API Integration

The frontend communicates with the vision API through a REST endpoint:

- **Endpoint**: `/api/card-recognition/identify`
- **Method**: POST
- **Body**: Form data with an 'image' field containing the card image
- **Response**: JSON array of card printings with details from Scryfall

Example response:
```json
{
  "printings": [
    {
      "id": "123",
      "name": "Black Lotus",
      "set": "lea",
      "setName": "Limited Edition Alpha",
      "collector_number": "232",
      "image_uris": {
        "small": "https://...",
        "normal": "https://...",
        "large": "https://..."
      },
      "mana_cost": "{0}",
      "type_line": "Artifact",
      "oracle_text": "{T}, Sacrifice Black Lotus: Add three mana of any one color.",
      "colors": [],
      "rarity": "rare",
      "prices": {
        "usd": "50000.00",
        "usd_foil": null
      }
    }
  ]
}
```

## Development Status

The system includes a fully functional web interface for card scanning and recognition. Current focus areas:
- Improving recognition accuracy for different card frames
- Enhancing collection management features
- Implementing mobile scanning capabilities
- Adding export and backup functionality
