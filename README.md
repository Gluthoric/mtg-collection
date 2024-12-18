gluth@gluth-P14s:~/mtg-collection$ git pull
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
gluth@gluth-P14s:~/mtg-collection$ git pull
# MTG Collection Manager

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

The card recognition service can identify Magic cards from images and retrieve detailed card information including all printings throughout Magic's history.

Example usage:
```python
python3 services/card-recognition/vision-api/card_identifier.py
# Enter the path to your card image when prompted
```

## Development Status

Currently implementing core functionality with a focus on accurate card recognition. The system will be expanded to include collection management features, mobile scanning, and more.
