import random
class Pokemon:
    """Representerar en Pokemon med namn, attack och hälsa,
    Varians står för hur mycket attackerna kan variera i en viss intervall
     """
    def __init__ (self, namn: str, attack: int, hp: int, varians: int) -> None:
        self.namn = namn
        self.attack = attack
        self.hp = hp
        self.max_hp = hp
        self.varians = varians #slagintervall för hur mycket skada en pokemon gör .
#Representerar en Pokemon med namn, attack och hälsa
    def __str__(self) -> str:
        return f"{self.namn}"

#                 FÖRKLARING TILL INTERVALL FUNKTION !
# Om attack är > 10 så blir attack ett slumpat tal mellan (attack - varians) och attack
# annars: Alltså om attack nivån på Pokemon inte är högre än 10 så blir 
# skadan ett slumpat tal mellan (attack - varians) (attack + varians)
# Alltså det är helt som vanligt, t.ex har du 8 i attack och varians på 4 kan du slå
# lägst 4 och högst 12. 
    def intervall(self) -> int:
        if self.attack > 10:
            low = self.attack - self.varians
            if low < 1:
                low = 1
            high = self.attack
            return random.randint(low, high -1)
        else:
            low = self.attack - self.varians
            if low < 1:
                low = 1
            high = self.attack + self.varians
        return random.randint(low, high)
        
            
#Slumpar slag mellan högsta och lägsta intervallet, den variabeln kallar vi för varians.
        #högsta = self.attack + self.varians
        #slumpa = random.randint(lägsta, högsta)
        #return slumpa

#Funktion för att undvika att hälsan kan få en negativ siffra vilket jag stötte på flera gånger
#Här säger vi istället att om hälsan(hp) är mindre än 0 så är hp 0.
    def klipp_hp(self) -> int:
        if self.hp < 0:
            self.hp = 0
##Detta är en koll för att se att HP nollställs efter varje strid.
    def is_alive (self) -> bool:
        """Returnerar True om HP är större än 0"""
        return self.hp > 0

    def copy_pokemon(self) -> "Pokemon":
        ny = Pokemon(self.namn, self.attack, self.hp, self.varians)
        ny.max_hp = self.max_hp
        return ny