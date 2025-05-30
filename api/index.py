# api/index.py
from flask import Flask, jsonify, render_template # Ensure render_template is imported
from cmf_scraper import get_financial_events
import os # <-- Import os

# Get the directory of the current file (index.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the templates folder, assuming it's one level up from api/
# Use os.path.normpath to handle potential double slashes correctly
TEMPLATE_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'templates')) # <-- Define template path

# Initialize Flask app, telling it where to find templates
app = Flask(__name__, template_folder=TEMPLATE_DIR) # <-- Pass template_folder argument

@app.route('/')
def home():
    return "Welcome to the CMF Financial Events API. Try /api/events"

@app.route('/api/events')
def events_api():
    print("Received request for /api/events. Attempting to scrape...")
    
    try:
        events = get_financial_events()
        print(f"Scraped {len(events)} events successfully.")
        
        return render_template("calendario.html", scrapedEventsData=events)
        
    except Exception as e:
        print(f"Error in /api/events endpoint: {e}")
        # Make sure to return the error with a 500 status code
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

# This block is for local development only and will not run on Vercel
if __name__ == "__main__":
    app.run(debug=True)
