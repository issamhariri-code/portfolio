"""
syfte:
den här filen hämtar all data för aktier, open,high,low,close + namn
all logik som pratar med API ligger här vi samlar varningar istället
för att krascha så appen kan visa data även om något saknas.

huvudfunktion:
fetch_prices(items, date)
tar emot en lista med tickers och ett datum
loopar varje ticker, hämtar open,high,low,close + företagsnamn
bygger en lista med poster
samlar varningar om något saknas
returnerar {"data": [...], "warnings": [...]} dict format

output-format:
{
    "data": [ {ticker, name, open, high, low, close, pct_change}, ... ],
    "warnings": ["Ingen data för TSLA", "NVDA saknar 'high'"]
}

regler:
max 10 tickers per gång (garanteras redan i valideringen).
inga exceptions ska gå vidare — bara warnings.
"""

# dataformat per post (exempel):
# { "ticker": "...", "name": "...", "open": x, "high": x, "low": x, "close": x, "pct_change": x }
# pct_change = (close - open) / open * 100

