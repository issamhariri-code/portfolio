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
from flask import Flask

def routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return "OK"
