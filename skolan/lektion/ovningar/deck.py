#Importera card
# Skapa en ny klass Deck
# I __init__(): gör en lista med alla kort H2, H3, H4 ... S13 och så vidare 52 kort totalt.
# Skapa loop
#C = Card(color, value)
#använd .append()
import random
from card import Card
class Deck:
    def __init__(self):
        self.cards = []
        for color in range(1, 5):  # 1-4 representerar H, R, K, S
            for value in range(1, 14):  # 1-13 representerar kortvärden
                self.cards.append(Card(color, value))

deck = Deck()   
cards = deck.cards          # Skapar kortleken
print(deck.cards[0].face)
random.shuffle(cards)
print(cards[0].face)