README — Kort instruktion för kollega

Syfte
-----
Jag har implementerat Card- och Deck-klasserna samt databasintegrationen för att spara spelresultat. Din uppgift är att skapa menyn som använder den här logiken.

Filer att ta med
-----------------
- deck.py       -> skapar däck (4 färger × 20 värden = 80 kort), blandar och sparar ett enkelt spel.
- card.py       -> definierar `Card`-klassen (har attributen `value` och `face`).
- databas_card.py -> hanterar SQLite (`kortspel.db`) och tillhandahåller `spara_resultat()`, `visa_statistik()` och `hamta_senaste()`.

Viktigt
-------
- Placera alla tre filer i samma mapp.
- Kör i Python 3.
- `databas_card.py` skapar `kortspel.db` i samma mapp första gången det körs.
- Om du vill bevara historik, inkludera även filen `kortspel.db` när du skickar materialet.

Vad du som kollega ska implementera (menyn)
------------------------------------------
- Skapa en meny (terminal/GUI) med ett val "Spela".
- När användaren väljer "Spela":
  - Importera och använd `Deck` från `deck.py`.
  - Blanda: `random.shuffle(d.cards)`.
  - Ta de två översta korten: `spelarkort = d.cards[0]`, `dator_kort = d.cards[1]`.
  - Bestäm vinnare genom att jämföra `value` (int).
  - Spara resultat: `databas_card.spara_resultat(spelarkort.face, dator_kort.face, vinnare)`.
  - Visa resultatet i menyn.

Förslag: enkel funktion att återanvända i menyn
---------------------------------------------
Kopiera gärna följande funktion in i menykoden för att återanvända spel-logiken:

```python
import random
from deck import Deck
from databas_card import spara_resultat

def spela_en_gang():
    d = Deck()
    random.shuffle(d.cards)
    if len(d.cards) < 2:
        return None
    spelar = d.cards[0]
    dator = d.cards[1]
    if spelar.value > dator.value:
        vinnare = 'spelare'
    elif spelar.value < dator.value:
        vinnare = 'dator'
    else:
        vinnare = 'oavgjort'
    spara_resultat(spelar.face, dator.face, vinnare)
    return spelar.face, dator.face, vinnare
```

Extra tips
----------
- Använd `databas_card.visa_statistik()` i menyn för att visa sammanfattning av vinster.
- Använd `databas_card.hamta_senaste(n)` för att lista de senaste spelen.
- Kontrollera att `Card` har `value` och `face` innan du använder dem.

Kontakt
-------
Om något inte fungerar eller om du vill att jag förbereder en färdig menyfil, säg till så kan jag skapa en exempelmeny (terminalbaserad) som ni kan använda.
