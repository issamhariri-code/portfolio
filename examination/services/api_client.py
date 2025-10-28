"""
Syfte: Hämta prisdata för varje ticker för ett valt datum,
Returnera lista med dataposter + eventuella varningar

Input: tickers [lista] exempelvis: [AAPL, TSLA]
date (str): yyyy-mm-dd

Output:
data: lista av poster med:
ticker, name, open, high, low, close, pct_change (ändring i procent)
varningar: lista av strängar

Metod:
Hämta prisinformation per ticker
beräkna procentändring om open/close finns tillgängligt
om data saknas - varning
vid api fel/404/timeout - varning sedan fortsätt 

Planering:
loopa igenom tickers med hämtat börs api
hämta data för varje ticker
skapa datapost och lägg i output
samla varningar

"""
# Dataformat per post (exempel):
# { "ticker": "...", "name": "...", "open": x, "high": x, "low": x, "close": x, "pct_change": x }
# pct_change = (close - open) / open * 100

