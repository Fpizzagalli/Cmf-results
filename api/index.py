# api/index.py
from flask import Flask, jsonify, render_template # <-- Import render_template
from cmf_scraper import get_financial_events
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the CMF Financial Events API. Try /api/events"

@app.route('/api/events')
def events_api():
    print("Received request for /api/events. Attempting to scrape...")
    
    try:
        events = get_financial_events()
        print(f"Scraped {len(events)} events successfully.")
        
        # Ensure 'templates' folder exists at the root level relative to where vercel runs the function
        # Flask will look for templates/calendario.html
        return render_template("calendario.html", scrapedEventsData=events)
        
    except Exception as e:
        print(f"Error in /api/events endpoint: {e}")
        # Return a proper error response for the client
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

# This `if __name__ == "__main__":` block only runs when you execute the script directly,
# not when Vercel runs it as a serverless function.
# You can keep it for local testing if you run `python api/index.py`
if __name__ == "__main__":
    app.run(debug=True)
