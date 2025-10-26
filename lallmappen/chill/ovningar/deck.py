#Importera card
# Skapa en ny klass Deck
# I __init__(): gör en lista med alla kort H2, H3, H4 ... S13 och så vidare 52 kort totalt.
# Skapa loop
#C = Card(color, value)
#använd .append()
import random
import databas_card
from card import Card
databas_card.skapa_databas()
class Deck:
    def __init__(self):
        self.cards = []
        for color in range(1, 5):  # 1-4 representerar H, R, K, S
            for value in range(1, 21):  # 1-20 representerar kortvärden
                self.cards.append(Card(color, value))
deck = Deck()   
cards = deck.cards          # Skapar kortleken
print(deck.cards[0].face)
random.shuffle(cards)
print(cards[0].face)

# --- Spara ett enkelt resultat i databasen ---
import databas_card

# Se till att tabellen finns
databas_card.skapa_databas()

# Ta de två översta korten som ett spel (spelare vs dator)
if len(cards) >= 2:
    spelar_kort = cards[0]
    dator_kort = cards[1]

    # Bestäm vinnare baserat på value (enkelt exempel)
    if getattr(spelar_kort, 'value', 0) > getattr(dator_kort, 'value', 0):
        vinnare = 'spelare'
    elif getattr(spelar_kort, 'value', 0) < getattr(dator_kort, 'value', 0):
        vinnare = 'dator'
    else:
        vinnare = 'oavgjort'

    # Spara resultatet i databasen
    databas_card.spara_resultat(spelar_kort.face, dator_kort.face, vinnare)
    print(f"Sparat resultat: {spelar_kort.face} vs {dator_kort.face} -> {vinnare}")