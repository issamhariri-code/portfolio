README: Integration mellan card.py, deck.py, meny.py och databasen
===============================================================

Syfte
-----
Detta dokument beskriver de minimala, icke-invasiva ändringar och tillägg som rekommenderas för att få era moduler `card.py` och `deck.py` att fungera smidigt ihop med en menymodul (`meny.py`) och en separat DB-modul. Inga ändringar har applicerats automatiskt — här är exakt vad du kan klistra in själv.

Designprincip
--------------
- Minimala ändringar: återanvänd befintlig kod så mycket som möjligt.
- Moduler ska inte skriva ut (print) vid import.
- Tydligt, litet API för `Deck`: `shuffle()`, `draw()`, `remaining()`, `as_dicts()`.
- `Card` erbjuder `to_dict()` för enkel serialisering till DB.

1) `card.py` — minimal tillägg
--------------------------------
Lägg in följande metod i klassen `Card` (direkt efter `def __str__(self):` eller längst ner i klassen):

```python
    def to_dict(self):
        """Returnerar en serialiserbar dict för DB/loggning."""
        return {"color": self.color, "value": self.value}
```

Varför: gör det enkelt för DB-koden att ta emot ett korts data utan att känna till interna attributnamn.

2) `deck.py` — små metoder (lägg in i klassen `Deck`)
-----------------------------------------------------
Lägg in dessa metoder i `Deck`-klassen (samma indentering som `__init__`):

```python
    def shuffle(self):
        """Blanda kortleken."""
        random.shuffle(self.cards)

    def draw(self):
        """Ta och returnera ett kort (Card) eller None om leken är tom."""
        if not self.cards:
            return None
        return self.cards.pop()

    def remaining(self):
        """Returnerar antal kort kvar i leken (int)."""
        return len(self.cards)

    def as_dicts(self):
        """Returnerar listan av kort som dicts (för DB/logg)."""
        return [getattr(c, "to_dict", lambda: {"color": c.color, "value": c.value})() for c in self.cards]
```

Valfritt men rekommenderat: flytta eventuella testutskrifter längst ner i filen under en guard:

```python
if __name__ == "__main__":
    deck = Deck()
    cards = deck.cards
    print(deck.cards[0].face)
    random.shuffle(cards)
    print(cards[0].face)
```

Denna guard förhindrar att `print`-satser körs när någon importerar `Deck` i `meny.py`.

3) Hur `meny.py` ska anropa (exempel)
--------------------------------------
Din meny (eller kollegan som skriver menyn) kan använda `Deck` och `Card` enligt detta mönster:

```python
from deck import Deck

deck = Deck()
deck.shuffle()

svar = input("Vill du dra ett kort? [j/n]: ").strip().lower()
if svar == "j":
    card = deck.draw()
    if card is None:
        print("Inga kort kvar i leken.")
    else:
        print("Du drog:", card)       # Card.__str__ bör vara läsbar, t.ex. "H 7"
        data = card.to_dict()         # För DB: {'color': 'H', 'value': 7}
        # skicka `data` vidare till DB-modulen
```

4) Databas (tredje kollegan)
-----------------------------
- DB-modulen bör ta emot en serialiserad struktur (t.ex. dict från `card.to_dict()`), komplettera med timestamp eller user_id och spara.
- Exempel på payload att spara:

```python
payload = card.to_dict()
payload.update({"user": user_id, "timestamp": datetime.utcnow().isoformat()})
# spara payload i SQL eller annat
```

5) Snabbtest i terminal (kopiera/klistra)
-----------------------------------------
Testa i samma mapp som filerna (eller ange rätt modul-sökväg):

```bash
python3 -c "from deck import Deck; d=Deck(); d.shuffle(); c=d.draw(); print('DROG:', c, getattr(c,'to_dict', lambda:None)())"
```

6) Checklista före integration
-------------------------------
- [ ] `card.py` innehåller endast Python-kod (inga markdown-fence ``` kvar).
- [ ] `card.py` har `to_dict()` om ni vill spara i DB.
- [ ] `deck.py` innehåller `shuffle`, `draw`, `remaining` (valfritt: `as_dicts`).
- [ ] Eventuella debug/print-rader i `deck.py` ligger under `if __name__ == '__main__':`.
- [ ] `meny.py` importerar bara `Deck` (`from deck import Deck`) och anropar `draw()`.
- [ ] DB-modulen tar emot dict från menyn och sparar.

7) Vanliga fallgropar
---------------------
- Om `deck.py` innehåller `print`/testkod utanför `__main__` kommer dessa att köras vid import och ge oväntade utskrifter i menyn.
- Om `card.py` av misstag innehåller textfencing (```) eller inte är ren Python så får ni SyntaxError vid import.
- Kontrollera att modulvägen är korrekt (samma mapp eller att mappen är en package med __init__.py om ni importerar från annan plats).

8) Om du vill att jag genererar
------------------------------
Säg vilken av dessa du vill ha som färdiga filer/snippar att klistra in (jag ändrar inget i repo):
- "patch" → jag visar exakt diff du kan göra.
- "meny" → färdigt `meny_sample.py` som din kollega kan klistra in.
- "README file" → jag har redan skapat den här filen `README_integration.md` i mappen och du kan öppna den.


---
README skapad i: /home/issam/git/skolan/lektion/ovningar/README_integration.md
Öppna filen när du vill granska eller dela med gruppen.