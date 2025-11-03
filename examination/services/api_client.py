"""
BörsLexikon hämtar riktig aktiedata från Marketstack API
ENKEL KOD FÖR PROGRAMMERING 2: Bara requests, ingen mock, ingen komplexitet
Fungerar för alla tickers (TSLA, AAPL, MSFT, osv) och alla datum
API-nyckel hårdkodad för enkelhet (ta bort i produktion)
"""

import datetime
import requests  # pip install requests

#API-NYCKEL – från Marketstack
API_KEY = "REDACTED_API_KEY"


# Lokala företagsnamn – fallback om API inte ger namn
company_names = {
    "AAPL": "Apple Inc.",
    "TSLA": "Tesla Motors",
    "NVDA": "Nvidia Corp",
    "MSFT": "Microsoft Corp",
    "AMZN": "Amazon",
    "GOOG": "Alphabet Inc (Google)",
    "PLTR": "Palantir Tech",
    "RCAT": "Red Cat Holdings",
    "ONDS": "Ondas Holdings"
}
# Omvänd uppslagning: företagsnamn -> ticker (för exakta namn som i company_names)
name_to_ticker = {v.lower(): k for k, v in company_names.items()}

# Enkla alias så korta namn funkar (lägg till fler vid behov)
# behöver rådata för x antal tickers annars behöver jag hämta större global api
# denna rådata gör att användaren får möjlighet att skriva 10 företagsnamn 
#utan tickers. På frontend delen index.html så finns det klargörande meddelande
# som visar vilka företagsnamn som funkar utan tickers alltså de nedanstående.
name_aliases = {
    "apple": "AAPL",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "google": "GOOG",
    "alphabet": "GOOG",
    "palantir": "PLTR",
    "red cat": "RCAT",
    "ondas": "ONDS",
}


"""räknar ut procentförändring från open till close"""
def compute_pct_change(open_price, close_price):
    if not open_price or open_price == 0 or not close_price:
        return None
    return round(((close_price - open_price) / open_price) * 100, 2)

"""hämtar företagsnamn eller använder ticker"""
def lookup_name(ticker):
    return company_names.get(ticker, ticker)

"""hämtar OHLC-data från Marketstack API"""
def fetch_from_marketstack(ticker, date):
    try:
        # Gör datum till sträng för API:et
        date_str = date.strftime("%Y-%m-%d")
        
        # Bygg URL och parametrar (enkelt GET-anrop)
        url = url = "https://api.marketstack.com/v1/eod"
        params = {
            "access_key": API_KEY,
            "symbols": ticker.upper(),
            "date_from": date_str,
            "date_to": date_str,
            "limit": 1  # Bara en dag behövs
        }
        
        # Skicka förfrågan (timeout för säkerhet)
        response = requests.get(url, params=params, timeout=10)
        
        # Kolla status och JSON
        if response.status_code != 200:
            print(f"API-fel för {ticker}: Status {response.status_code}")
            return None
        
        data = response.json()
        if not data.get("data"):
            return None
        
        # ta första enda posten
        post = data["data"][0]
        
        # extrahera priser använd .get() för säkerhet
        open_ = post.get("open")
        high = post.get("high")
        low = post.get("low")
        close = post.get("close")
        
        if None in (open_, high, low, close):
            return None
        
        return {
            "open": float(open_),
            "high": float(high),
            "low": float(low),
            "close": float(close)
        }
    except Exception as e:
        print(f"API-fel ({ticker}): {e}")
        return None

"""hämta pris för ett datum bara från API"""
def fetch_quote_for_date(ticker, date):
    return fetch_from_marketstack(ticker, date)

"""huvudfunktion returnerar tabell + varningar"""
def fetch_prices(items, date):
    """Hämtar priser för en lista av tickers/namn på ett specifikt datum.
       Returnerar { "data": [...], "warnings": [...] }.
    """
    rows = []
    warnings = []

    # 1) Datumhantering (till date-objekt)
    if isinstance(date, str):
        try:
            parsed_date = datetime.date.fromisoformat(date)  # YYYY-MM-DD
        except ValueError:
            warnings.append(f"Ogiltigt datum: {date}")
            return {"data": [], "warnings": warnings}
    else:
        parsed_date = date

    # översätt användarens inmatning till tickers
    cleaned_items = []
    for raw in items:
        val = (raw or "").strip()
        if not val:
            continue

        lower = val.lower()

        # exakt företagsnamn, t.ex. "apple inc."
        if lower in name_to_ticker:
            cleaned_items.append(name_to_ticker[lower])
            continue

        # alias, t.ex. "apple", "tesla"
        if lower in name_aliases:
            cleaned_items.append(name_aliases[lower])
            continue

        # annars: om det ser ut som en ticker (A–Z/0–9/.-) ta som ticker
        if all(ch.isalnum() or ch in ".-" for ch in val):
            cleaned_items.append(val.upper())
        else:
            warnings.append(f"Okänt företagsnamn: “{val}”. Ange tickern (t.ex. AAPL).")

    #  begränsat antal för enkelhet
    if len(cleaned_items) > 10:
        warnings.append("Max 10 tickers/företagsnamn åt gången. Visar första 10.")
        cleaned_items = cleaned_items[:10]

    # hämta priser per ticker
    for ticker in cleaned_items:
        quote = fetch_quote_for_date(ticker, parsed_date)  # hämtar open/high/low/close
        if not quote:
            warnings.append(f"Ingen data för {ticker} på {parsed_date}")
            continue

        name = lookup_name(ticker)  # visar snyggt företagsnamn om vi har det
        o, h, l, c = quote["open"], quote["high"], quote["low"], quote["close"]
        pct = compute_pct_change(o, c)

        rows.append({
            "ticker": ticker,
            "name": name,
            "open": round(o, 2),
            "high": round(h, 2),
            "low": round(l, 2),
            "close": round(c, 2),
            "pct_change": pct
        })

    return {"data": rows, "warnings": warnings}
