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

# rådatahantering här finslipar vi arbetat, trimmar,splittar på inputs, filterar bort tomma inputs
# kollar max antal tickers och sparar i rätt lista, hanterar datumfel.

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
    if tickers_input is None or "":
        errors.append("Ange minst en ticker eller företagsnamn")
        return result
    items = tickers_input.split(",") #tar  bort kommatecken
    cleaned_items = []
    for item in items:
        trimmed_item = item.strip() #trimmar bort whitespace
    cleaned_items.items.append(trimmed_item)  #lägger in det trimmade i listan
    final_items = [] #skapar ny lista
    for i in cleaned_items: #loopar igenom cleaned_items som inte är tom
        if i != "":  # städar upp tomma strängar
           final_items.append(i)  #appendar in i listan final_items
    if final_items == []: #om listan är tom
        errors.append("Ange minst en ticker eller företagsnamn") #felmeddelande
        return result
    if len(final_items) > max_items: #om användaren skriver in fler än vad max_items tillåter som är 10
        errors.append("Max 10 tickers är tillåtna") #felmeddelande
        return result
    clean["raw_items"] = final_items
    new_list = []
    for item in clean["raw_items"]:
        upper_item = item.upper() #checkar stora versaler
        new_list.append(upper_item) #sparar det i listan new_list