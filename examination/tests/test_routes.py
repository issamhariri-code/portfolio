"""
GET 
ska svara 200
ska innehålla formulärets fält (tickers, datum ,annat)
använder index.html template

POST - ogiltig input
om datum saknas - visar felmeddelande på index.html
ingen ticker angett - visar felmeddelande
för många tickers - visar fel
datum i framtiden - visar fel
vid fel ska inte sidan krascha utan gå igenom index igen


POST - giltig input
anropar validation fil - ok
anropar api_client fil
renderar result.html template
result.html innehåller 
(datum, perspektiv, tabellhuvud, rader för varje ticker med data)


POST - varning från api_client
om ticker saknar data - varning syns i result.html 
övriga tickers visas normalt

output:
response status
rätt template används
rätt text i HTML
"""