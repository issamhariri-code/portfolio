"""
testar att api_client hanterar flera tickers korrekt, räknar procent
samlar varningar utan krasch.

tester:
flera tickers returnerar samma antal data poster
varje datapost innehåller open/high/low/close/ticker/date
pct_change räknas korrekt

om en ticker saknar data:
ge varning med rätt felmeddelande
övriga tickers ska fortfarande finnas i datan

404 eller api-fel för ticker:
varning läggs till
webbapplikationen fortsätter för nästa ticker

hantering av None värden:
om open/close är None blir pct_change None
data finns kvar med felmeddelande

output blir:
data som lista av dataposter
varningar (felmeddelanden) som lista av strängar
"""

#api_client får aldrig krascha för en enskild ticker
#ge korrekt datastruktur, procent, och felmeddelanden.