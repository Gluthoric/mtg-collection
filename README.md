# MTG Collection Manager

A comprehensive Magic: The Gathering collection management system with card recognition capabilities.

## Features

- Card recognition using Google Cloud Vision API
- Multiple services for different aspects of collection management
- Support for various card frames and sets
- Integration with Scryfall API for accurate card information

## Project Structure

- `services/card-recognition/vision-api`: Card recognition service using Google Cloud Vision
- `services/collection-api`: API for managing collection data
- `services/mobile-scanner`: Mobile scanning capabilities
- `services/qr-service`: QR code generation and scanning
- `frontend`: Web and mobile client applications
- `database`: Database migrations and models
- `docs`: Project documentation
- `utils`: Utility scripts and tools

## Setup

1. Install dependencies:
```bash
cd services/card-recognition/vision-api
python3 -m venv venv
source venv/bin/activate
pip install google-cloud-vision requests
```

2. Configure Google Cloud Vision API:
- Set up a Google Cloud project
- Enable the Vision API
- Create a service account and download credentials
- Save credentials as `service_account.json` in the project root

## Usage

The card recognition service can identify Magic cards from images and retrieve detailed card information including all printings throughout Magic's history.

Example usage:
```python
python3 services/card-recognition/vision-api/card_identifier.py
# Enter the path to your card image when prompted
```

## Development Status

Currently implementing core functionality with a focus on accurate card recognition. The system will be expanded to include collection management features, mobile scanning, and more.
