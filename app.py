from flask import Flask, render_template
from cmf_scraper import get_financial_events

app = Flask(__name__)

@app.route("/")
def home():
    events = get_financial_events()
    return render_template("calendario.html", scrapedEventsData=events)

if __name__ == "__main__":
    app.run(debug=True)
