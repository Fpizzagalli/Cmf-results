from flask import Flask, jsonify
from cmf_scraper import get_financial_events # Import your scraper

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the CMF Financial Events API. Try /api/events"

@app.route('/api/events')
def events_api():
    events = get_financial_events()
    return jsonify(events)
