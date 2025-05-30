# api/index.py
from flask import Flask, jsonify
from cmf_scraper import get_financial_events
import os # Import os for environment variables

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the CMF Financial Events API. Try /api/events"

@app.route('/api/events')
def events_api():
    print("Received request for /api/events. Attempting to scrape...") # <-- ADD THIS LOG

    # You can also print headers received by Flask for debugging
    # print(f"Request Headers: {dict(request.headers)}") 

    try:
        events = get_financial_events()
        print(f"Scraped {len(events)} events successfully.") # <-- ADD THIS LOG
        return jsonify(events)
    except Exception as e:
        print(f"Error in /api/events endpoint: {e}") # <-- ADD THIS LOG
        # IMPORTANT: Re-raise the exception or return an error response
        # so Vercel captures the 502/server error properly.
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

# ... (rest of your code, if any)
