"""
Syfte: Filen ska validera inmatarens indata som är tickers + datum och ge
tydliga felmeddelanden.
Input:
tickers_input (str), exempelvis: AAPL, tsla, Nvidia (lower,upper, hela namnet)
date_input(str), exempelvis: 2025 - 10 - 22

Output:
valid (bool)
errors (lista med strängar)

Felmeddelanden:
Ange ett datum
Ogiltigt datum
Datum får inte vara före 2022 - 11 - 01
Datum får inte vara i framtiden
Max 10 tickers tillåtna åt gången
Ogiltiga tecken i {värde}

Planen är att:
kontrollera datum, dela upp tickers, kontrollera antal och format, returnera
"""
# Regler:
# datum: inte tomt, inte före 2022-11-01, inte efter idag
# tickers: minst 1, max 10, korrekta tecken
# tomma poster tas bort, versaler normaliseras

# Här lägger vi funktionerna senare (validate_input)
