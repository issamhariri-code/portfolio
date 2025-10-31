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
import datetime

# Regler:
# datum: inte tomt, inte före 2022-11-01, inte efter idag
# tickers: minst 1, max 10, korrekta tecken
# tomma poster tas bort, versaler normaliseras

# Här lägger vi funktionerna senare (validate_input)

#minsta tillåtna datum
min_date = datetime.date(2022, 11, 1)
#max antal ticker per sökning
max_items = 10

def validate_input(tickers_input, date_input):
    errors = []
    clean = {"date": None, "raw_items": [], "limit": max_items}
    result = {"valid": False, "errors": errors, "clean": clean}
    if date_input is None:
        errors.append("Ange ett datum")
        return result
    elif date_input == "":
        errors.append("Ange ett datum")
        return result
    try:
        parsed_date = datetime.date.fromisoformat(date_input)
        clean["date"] = parsed_date
        today = datetime.date.today()
        if clean["date"] < min_date:
            errors.append("Datum får inte vara före 2022-11-01")
            return result
        if clean["date"] > today:
            errors.append("Datum får inte vara i framtiden")
            return result
    except ValueError:
        errors.append("Ogiltig datumformat. Använd YY-MM-DD")
        return result

