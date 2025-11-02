"""
den här filen hämtar all data för aktier, open,high,low,close + namn
all logik som pratar med API ligger här vi samlar varningar istället
för att krascha så appen kan visa data även om något saknas.

huvudfunktion:
fetch_prices(items, date)
tar emot en lista med tickers och ett datum
loopar varje ticker, hämtar open,high,low,close + företagsnamn

regler:
max 10 tickers per gång (garanteras redan i valideringen).
inga exceptions ska gå vidare — bara warnings.
"""
import datetime
company_names = {"AAPL": "Apple Inc.", #lokalt lexikon med rådata
                 "TSLA": "Tesla Motors",
                 "NVDA": "Nvidia Corp",
                 "MSFT": "Microsoft Corp",
                 "AMZN": "Amazon",
                 "GOOG": "Aplhabet Inc (Google)",
                 "PLTR": "Palantir Tech",
                 "RCAT": "Red Cat Holdings",
                 "ONDS": "Ondas Holdings"}

mock_db = {
    ("AAPL", datetime.date(2025, 10, 22)): {"open": 172.0, "high": 175.0, "low": 171.0, "close": 172.0},
    ("TSLA", datetime.date(2025, 10, 22)): {"open": 420.0, "high": 422.0, "low": 418.0, "close": 420.0},
    ("NVDA", datetime.date(2025, 10, 22)): {"open": 181.0, "high": 183.0, "low": 177.0, "close": 178.0}
}

"""räknar ut ändring i procent mellan open och close
return float tex 123 eller None om open och close saknas eller om open är 0"""
def compute_pct_change(open_price, close_price):
    if open_price is None:
        return None
    if close_price is None:
        return None
    if open_price == 0:
        return None
    diff = close_price - open_price
    pct = (diff/open_price) * 100
    return pct

"""slår upp företagsnamn eller ticker, return str (namn) eller None om okänt"""
def lookup_name(ticker): 
    name = company_names.get(ticker) #ticker redan upper från validation
    return name #blir str eller None

"""hämta open,high,low,close för ett datum och ticker
returnerar med dict eller None om inge data finns"""
def fetch_quote_for_date(ticker, date):
    try:
        # skapa en nyckel (ticker, date)
        key = (ticker, date)
        # hämta data från mock_db med get()
        post = mock_db.get(key)    
        open_ = post.get("open")
        high = post.get("high")
        low = post.get("low")
        close = post.get("close")
        return {"open": open_,
                "high": high,
                "low": low,
                "close": close}
    except Exception: #fångar alla oväntade fel för att va extra trygg
        return None

"""huvudfunktion som tar emot lista av tickers + datum, loopar igenom
hämtar open,high,low,close och räknar ut pct_change, samlar varningar
bygger lista för output"""
#steg i fetch_prices
#1. loopa tickers    2. hämta quote    3. hämta namn 
#4. hantera saknade fält    5. räkna pct_change
#6. bygg en rad    7. samla varningar    8. returnera data + warnings
def fetch_prices(items, date):
    rows = []
    warnings = []
    for ticker in items:
        quote = fetch_quote_for_date(ticker, date)
        if quote is None:
            warnings.append(f"Ingen data för {ticker} på {date}")
            continue
        name = lookup_name(ticker)
        high = quote.get("high")
        open_ = quote.get("open")
        close = quote.get("close")
        low = quote.get("low")
        if open_ is None or high is None or low is None or close is None:
            warnings.append(f"Ofullständig data för {ticker} på {date}")  

"""läser api värden utan att krascha, returnar värde eller default"""
def safe_get(d, key, default=None):
    if d is None:
        return default
    return d.get(key, default)