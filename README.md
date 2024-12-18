# MTG Collection Manager

A comprehensive Magic: The Gathering collection management system that combines card recognition capabilities with advanced collection tracking and organization features.

## Features

- Card recognition using Google Cloud Vision API
- Collection tracking and organization
- CSV-based set management with Scryfall integration
- Web interface for collection management
- Multiple services for different aspects of collection management
- Support for various card frames and sets
- QR code generation and scanning
- Mobile scanning capabilities

## Project Structure

```
mtg-collection/
├── database/               # Database migrations and models
├── docs/                   # Project documentation
│   ├── api/               # API documentation
│   ├── setup/             # Setup guides
│   └── usage/             # Usage guides
├── frontend/              # React/TypeScript web application
├── services/              # Microservices
│   ├── card-recognition/  # Card recognition service
│   │   ├── vision-api/   # Google Cloud Vision integration
│   │   ├── processor/    # Image processing
│   │   └── bulk-scanner/ # Bulk scanning capability
│   ├── collection-api/    # Collection management API
│   ├── mobile-scanner/   # Mobile scanning application
│   └── qr-service/       # QR code generation and scanning
├── storage/               # Data storage
│   ├── backups/          # Database backups
│   ├── box-contents/     # Box inventory data
│   ├── card-images/      # Card image storage
│   └── organized-sets/   # Organized set data
└── utils/                 # Utility scripts and tools
    ├── scripts/          # Python scripts for data processing
    │   └── collection/   # Collection management scripts
    └── tools/            # Helper tools
```

## Collection Management Features

### Set Organization
- Comprehensive set tracking
- Support for various set types:
  - Standard sets
  - Commander sets
  - Masters sets
  - Special sets
  - Promotional sets
- CSV-based data management
- Scryfall data integration

### Card Recognition
- Google Cloud Vision API integration
- Support for different card frames
- Bulk scanning capabilities
- Mobile scanning support

### Data Management
- SQLite database for collection storage
- CSV data processing and organization
- Regular backups
- Data export capabilities

## Setup

1. Install Dependencies:
```bash
# Frontend
cd frontend
npm install

# Card Recognition Service
cd services/card-recognition/vision-api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Collection Scripts
cd utils/scripts/collection
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure Google Cloud Vision API:
- Set up a Google Cloud project
- Enable the Vision API
- Create a service account and download credentials
- Save credentials as `service_account.json` in the project root

3. Initialize Database:
```bash
# Initialize collection database
python utils/scripts/collection/collection_tracker.py --init
```

## Usage

### Collection Management
```bash
# Process and organize new sets
python utils/scripts/collection/cleanup_csvs.py

# Add Scryfall data to sets
python utils/scripts/collection/add_scryfall_bulk_parallel.py

# Verify Scryfall data
python utils/scripts/collection/verify_scryfall_data.py
```

### Card Recognition
```bash
# Run card recognition service
python services/card-recognition/vision-api/card_identifier.py
```

### Web Interface
```bash
# Start frontend development server
cd frontend
npm run dev

# Start collection API service
cd services/collection-api
python app.py
```

## Development

The project uses a microservices architecture with the following components:

- Frontend: React/TypeScript with Vite
- Card Recognition: Python with Google Cloud Vision
- Collection API: Python-based REST API
- Mobile Scanner: React Native application
- QR Service: Node.js service

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

[Add License Information]
