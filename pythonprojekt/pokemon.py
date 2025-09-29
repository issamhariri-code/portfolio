class Pokemon:
    def __init__(self, namn, attack, hp):
        self.namn = namn
        self.attack = attack
        self.hp = hp
        self.max_hp = hp

    def is_alive(self):
        if self.hp > 0:
            return True
        else:
            return False
        
        