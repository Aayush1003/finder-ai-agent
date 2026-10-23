# finder-ai-agent

A lightweight AI-style marketplace finder that helps discover products across leading e-commerce sources such as Amazon, Flipkart, and Meesho.

## Features

- Search by product name or category
- Compare product prices and delivery details
- Rank results by relevance
- View recommendations from multiple marketplaces
- Clean, responsive UI

## Run locally

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python app.py
   ```
4. Open: http://localhost:5000

## Example searches

- wireless earbuds
- running shoes
- kitchen appliance
- backpack
- smartwatch

## Project structure

- `app.py` — Flask application
- `templates/index.html` — frontend layout
- `static/` — CSS and JavaScript
- `data/products.json` — product catalog used by the demo finder
