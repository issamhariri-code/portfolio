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
#Skapar funktion så att en pokemon gör skada mellan ett visst intervall för mer användarvänlighet.  
    def intervall(self) -> int:
        lägsta = self.attack - self.varians
        if lägsta < 1:
            lägsta = 1
#Slumpar slag mellan högsta och lägsta intervallet, den variabeln kallar vi för varians.
        högsta = self.attack + self.varians
        slumpa = random.randint(lägsta, högsta)
        return slumpa

#Funktion för att undvika att hälsan kan få en negativ siffra vilket jag stötte på flera gånger
#Här säger vi istället att om hälsan(hp) är mindre än 0 så är hp 0.
    def klipp_hp(self) -> int:
        if self.hp < 0:
            self.hp = 0

    def is_alive (self) -> bool:
        """Returnerar True om HP är större än 0"""
        return self.hp > 0
