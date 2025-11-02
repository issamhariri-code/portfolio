"""
Hur appens GET och POST routes ska fungera.
GET "/"
visar index.html
skickar ev felmeddelanden och tidigare inmatning

POST "/stocks"
hämtar tickers_input, date_input och perspective
validering sker via validation.py
om fel anges, renderar index.html igen med error
om ok anges, skicka rensade tickers och datum till api_client
rendera result.html med sammanfattning,data och felmeddelanden.

404
visar 404.html med a=href länk tillbaka till "/"
"""
from flask import Flask, render_template, request
from services import api_client
import datetime
from services import validation

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
            "tickers_input":tickers_input,
            "perspective": perspective,
            "table_rows": table_rows,
            "title": title_text,
            "date_input": date_input
        }
        return render_template("index.html", context)
    
    @app.route("/", methods=["POST"])
    def handle_post():
        messages = []

        tickers_input = request.form.get("tickers")
        date_input = request.form.get("date")
        perspective = request.form.get("perspective")
        
        if tickers_input is None or tickers_input.strip() == "":
            messages.append("Ange minst en ticker")
            context = {
                "messages": messages,
                "tickers_input": "",
                "date_input": date_input,
                "perspective": perspective,
                "table_rows": [],
                "title": ""}
            return render_template("index.html", context)
        
        tickers_input = tickers_input.strip()
        tickers_input = tickers_input.upper()
        ticker_list = tickers_input.split(",")

        if date_input is None or date_input == "":
            messages.append("Välj datum")
        
        if messages:
            context = {
                "messages": messages,
                "tickers_input": tickers_input,
                "date_input": date_input,
                "perspective": perspective,
                "table_rows": [],
                "title": ""}
            return render_template("index.html", context)
        
        result = api_client.fetch_prices(ticker_list, date_input)
        rows = result["data"]
        warnings = result["warnings"]
        
        if len(warnings) > 0:
            messages.extend(warnings)
        
        if len(rows) > 0:
            messages.append("Hittade n rader")
        else:
            messages.append("Ingen data hittades")

        title_text = "Priser för " + date_input
        context = {
            "messages": messages,
            "tickers_input": tickers_input,
            "date_input": date_input,
            "perspective": perspective,
            "table_rows": rows,
            "title": title_text}
        return render_template("index.html", context)