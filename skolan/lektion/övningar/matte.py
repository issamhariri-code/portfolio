# skapa addera(tal1, tal2) returnera svaret
def addera(tal1, tal2):
    return tal1 + tal2

#skapa subtrahera(tal1, tal2) returnera svaret
def subtrahera(tal1, tal2):
    return tal1 - tal2

# skapa multiplicera(tal1, tal2) returnera svaret
def multiplicera(tal1, tal2):
    return tal1 * tal2

# skapa dividera(tal1, tal2) returnera svaret
def dividera(tal1, tal2):
    if tal2 == 0:
        return "Kan inte dividera med noll"
    return tal1 / tal2

# Skapa ny funktion som heter matte(40, 5)
# den funktionen ska skriva ut alla andra
# exempel rad1 : Addera = 45
# exempel rad2 : Subtrahera = 35
# exempel rad3 : Multiplicera = 200
# exempel rad4 : Dividera = 8

def matte(tal1, tal2):
    print("Addera =", addera(tal1, tal2))
    print("Subtrahera =", subtrahera(tal1, tal2))
    print("Multiplicera =", multiplicera(tal1, tal2))
    print("Dividera =", dividera(tal1, tal2))

if __name__ == "__main__":
    pass
else:
    print("__name__ =" + __name__)
    