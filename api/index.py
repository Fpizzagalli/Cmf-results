
from flask import Flask, jsonify, render_template
from cmf_scraper import get_financial_events
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'templates')) 

# Initialize Flask app, telling it where to find templates
app = Flask(__name__, template_folder=TEMPLATE_DIR)

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
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
