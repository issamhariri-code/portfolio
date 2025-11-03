"""
Hur appens GET och POST routes ska fungera.
GET "/"
visar index.html, result.html, about.html samt 404.html
skickar ev felmeddelanden och tidigare inmatning

POST "/stocks"
hämtar tickers_input, date_input och perspective
validering sker via validation.py
om fel anges, renderar index.html igen med error
skickar resultat via result.html
lite info endpoint via about.html
404 fångar upp felaktig endpoint
om ok anges, skicka rensade tickers och datum till api_client
rendera result.html med sammanfattning,data och felmeddelanden.

404
visar 404.html med a=href länk tillbaka till startsidan.
"""
from flask import Flask, render_template, request, jsonify
from services import api_client
from services import validation
import requests
from datetime import datetime

def routes(app):
    @app.route('/', methods=['GET'])
    def index():
        messages = []
        tickers_input = ""
        date_input = ""
        perspective = ""

        table_rows = []
        title_text = ""
        context = {
            "messages": messages,
            "tickers_input": tickers_input,
            "perspective": perspective,
            "table_rows": table_rows,
            "title": title_text,
            "date_input": date_input
        }
        return render_template("index.html", **context)
    
    @app.route('/about', methods=['GET'])
    def about():
        context = {
            "title": "Om BörsLexikon",
            "messages": [],
            "tickers_input": "",
            "date_input": "",
            "perspective": "",
            "table_rows": []}
        return render_template("about.html", **context)


    @app.errorhandler(404)
    def handle_404(error):
        return render_template("404.html"), 404
    
    @app.route("/", methods=["POST"])
    def handle_post():
        messages = []

        tickers_input = request.form.get("tickers")
        date_input = (request.form.get("date") or "").strip()
        perspective = request.form.get("perspective")

        # om en ticker saknas
        if tickers_input is None or tickers_input.strip() == "":
            messages.append("Ange minst en ticker")
            context = {
                "messages": messages,
                "tickers_input": "",
                "date_input": date_input,
                "perspective": perspective,
                "table_rows": [],
                "title": ""
            }
            return render_template("index.html", **context)
        
        # normalisera tickers med trimmning
        tickers_input = tickers_input.strip().upper()
        ticker_list = [t.strip() for t in tickers_input.split(",") if t.strip() != ""]
        if len(ticker_list) == 0:
            messages.append("Välj minst en ticker")
            context = {
                "messages": messages,
                "tickers_input": tickers_input,
                "date_input": date_input,
                "perspective": perspective,
                "table_rows": [],
                "title": ""
            }
            return render_template("index.html", **context)

        # datum validering
        if date_input == "":
            messages.append("Välj datum")
            context = {
                "messages": messages,
                "tickers_input": tickers_input,
                "date_input": date_input,
                "perspective": perspective,
                "table_rows": [],
                "title": ""
            }
            return render_template("index.html", **context)
        
        if validation.is_valid_date(date_input) is False:
            messages.append("Ogiltigt datumformat (YYYY-MM-DD)")
            context = {
                "messages": messages,
                "tickers_input": tickers_input,
                "date_input": date_input,
                "perspective": perspective,
                "table_rows": [],
                "title": ""
            }
            return render_template("index.html", **context)

        # API-anrop som fångar fel
        try:
            result = api_client.fetch_prices(ticker_list, date_input)
        except Exception:
            messages.append("Tekniskt fel - försök igen")
            context = {
                "messages": messages,
                "tickers_input": tickers_input,
                "date_input": date_input,
                "perspective": perspective,
                "table_rows": [],
                "title": ""
            }
            return render_template("index.html", **context)
        
        rows = result["data"]
        warnings = result["warnings"]
        if warnings:
            messages.extend(warnings)

        # lägg till rad count i messages
        if rows:
            messages.append(f"Hittade {len(rows)} rader")
        else:
            messages.append("Ingen data hittades")

        # bygger context för result.html
        labels = {"daily": "Daglig", "weekly": "Veckovis"}
        perspective_label = labels.get(perspective, "")
        result_context = {
        "title": "Priser för " + date_input,
        "date": date_input,
        "perspective_label": perspective_label,
        "count": len(rows),
        "messages": messages,
        "data": rows,
        "empty": len(rows) == 0}


        return render_template("result.html", **result_context)
    
app = Flask(__name__)
routes(app)

if __name__ == "__main__":
    app.run(debug=True)
