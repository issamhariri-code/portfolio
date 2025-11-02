"""
formatera siffror för visning i tabellen.

input:
prisvärden (float eller None)
procentvärden (float eller None)
Output:
färdiga strängar för UI, exempelvis:
123.45,    -0.82%,       1.2%
"""
# Prisformat:
# två decimaler
# returnera sträng
# Procentformat:
# lägg till % i slutet
# visa − tecken vid behov

#mapping av perspektiv , visas i result.html
#variabler
#price_asc = pris stigande
#price_desc = pris fallande
#pct_asc = förändring i procent stigande
#pct_desc = förändring i procent fallande
#top_gainers = top 3 vinnare
#top_loosers = topp 3 förlorare
