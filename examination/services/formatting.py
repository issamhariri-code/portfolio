"""
Syfte:
Formatera numeriska värden för visning i tabellen.

Input:
prisvärden (float eller None)
procentvärden (float eller None)

Output:
färdiga strängar för UI, ex:
123.45
-0.82%
1.2%

Plan:
avrunda priser till 2 decimaler
avrunda procent till 1-2 decimaler
hantera None-värden (returnera tom sträng eller "—")
"""
# Prisformat:
# - två decimaler
# - returnera sträng
# Procentformat:
# - lägg till "%" i slutet
# - visa +/− tecken vid behov
# None:
# - om värde saknas → använd "—" eller tom sträng

