# MTG Collection Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A comprehensive Magic: The Gathering collection management system that combines card recognition capabilities with advanced collection tracking and organization features.

## Features

- Card recognition using Google Cloud Vision API
- Collection tracking and organization
- CSV-based set management with Scryfall integration
- Web interface for collection management
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

### Backend Setup

1. Set up the Flask API:
```bash
cd services/collection-api
python3 -m venv venv
source venv/bin/activate
pip install flask python-dotenv
```

2. Start the Flask server:
```bash
python app.py
```

The API will be available at http://localhost:5000

### Frontend Setup

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Create a .env file with:
```
VITE_API_URL=http://localhost:5000
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

### Card Recognition Setup

1. Install Dependencies:
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

### Collection Management

1. Access the web interface at http://localhost:5173
2. Browse your collection by sets
3. Add cards using the scanner or manual entry
4. Track quantities and foils
5. View collection statistics

### Card Recognition

The card recognition service can identify Magic cards from images and retrieve detailed card information including all printings throughout Magic's history.

Example usage:
```python
python3 services/card-recognition/vision-api/card_identifier.py
# Enter the path to your card image when prompted
```

### Testing

1. Test the API:
```bash
curl http://localhost:5000/api/stats
```

2. Test the frontend connection:
- Open browser dev tools
- Check Network tab for API calls
- Verify responses from backend

### Common Issues

1. If the frontend can't connect to the API:
- Check that both servers are running
- Verify the VITE_API_URL in .env
- Check browser console for CORS errors

2. If the database isn't found:
- Verify the database path in app.py
- Check file permissions

## Development Status

Currently implementing core functionality with a focus on accurate card recognition. The system will be expanded to include collection management features, mobile scanning, and more.
