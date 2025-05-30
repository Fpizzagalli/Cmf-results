# api/index.py
from flask import Flask, jsonify
from cmf_scraper import get_financial_events # Import your scraper

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the CMF Financial Events API. Try /api/events"

@app.route('/api/events')
def events_api():
    events = get_financial_events()
    return render_template("calendario.html", scrapedEventsData=events)
    #return jsonify(events)
if __name__ == "__main__":
    app.run(debug=True)

# Vercel requires a `handler` or `app` variable. For Flask, it's `app`.
# For a simple HTTP handler (without Flask/Django), you'd define `handler`.
# e.g., from http.server import BaseHTTPRequestHandler; class handler(BaseHTTPRequestHandler): ...
