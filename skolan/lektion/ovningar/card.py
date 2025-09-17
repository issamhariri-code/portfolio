#Skapa en klass för ett spelkort
#Minsta antal attribut är färg och värde
# __init__ ska lägga värdena i color och value
#Skapa en instans av klassen och skriv ut färg och värde
#Färger : Färger = "Hjärter", "Ruter", "Klöver", "Spader" = "H", "R", "K", "S"
#Värden: Värden = "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
import random
card_type = ["H", "R", "K", "S"]
class Card:
    def __init__(self, color: int, value: int):
        if color == 1:
            self.color = "H"
        elif color == 2:
            self.color = "R"
        elif color == 3:
            self.color = "K"
        elif color == 4:
            self.color = "S"
        else:
            print("Felaktig färg")
            self.color = None
            
        if 1 <= value <= 13:
            self.value = value
        else:
            print("Felaktigt värde")
            self.value = None

        self.face = f"{self.color} {self.value}"

    def __str__(self):   # <-- OBS! Måste vara indenterad här
        return f"{self.color} {self.value}"

#kollar att value är mellan 1-13
# kolla att color är "H", "R", "K", "S"
#Om inte ska ett felmeddelande skrivas ut
#Ska lägga variablerna i self variablerna