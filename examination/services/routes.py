"""
syfte:
beskriva hur appens webbflöde (GET/POST) ska fungera.

flöde:
GET/:
visar startsidan (index.html)
innehåller formulär:
tickers
datum
perspektiv
felmeddelanden

  POST /stocks :
tar emot formulärdata
skickar allt till validation.py
om valideringen hittar fel:
rendera index.html igen
visa errors-listan

om valideringen godkänns:
skicka raw items + data till api_client
ta emot data + varningar
formatting.py används vid tabellvisning
rendera result.html med:
sammanfattning
tabellhuvuden
rader med data
varningar

404-hantering:
egen template 404.html ska användas
användaren kan klicka tillbaka till startsidan via a=href

Plan:
denna fil är endast planering
riktig routing läggs senare i application/__init__.py och application/app.py
services ska inte ha Flask-kod, endast beskriva flödet
"""
