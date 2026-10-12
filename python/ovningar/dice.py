#försök komma på attribut för en tärning
#objekt - objektet
#class - ritning till objektet
#instans - varianter av ett objekt
#self. - talar om att det är ett attribut som hör till objektet
import random
class Dice:
    def __init__(self):
        self.material = "plastic"
        self.color = "black"
        self.sidor = 6
        self.vikt = 4 #gram
        self.form = "cube"

#försök att komma på saker man kan göra med den

    def __init__(self, sidor: int = 6):
        self.sidor = sidor


    def rulla(self):
        return random.randint(1, self.sidor)