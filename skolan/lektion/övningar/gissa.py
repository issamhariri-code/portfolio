#ta fram ett slymptal mellan 1 och 100 med random.randint(a, b)
# Be om en gissning med input från användaren
# Om inte rätt tal, tala om om det är för högt eller för lågt
# Ny gissning
# Annars:
# Avsluta om användaren gissar rätt, skriv ut "Grattis du gissade rätt!" 
import random
def gissa():
    try:


        tal = random.randint(1, 100)
        antal = 1
        gissning = None
        while gissning != tal:
            gissning = int(input("Gissa ett tal mellan 1 och 100: "))
            if gissning < tal:
                antal += 1
                print("För lågt! Försök igen.")
            elif gissning > tal:
                antal += 1
                print("För högt! Försök igen.")
            else:
                print(f"Grattis du gissade rätt! Du hade antal {antal} försök!")
    except ValueError:
        print("Ange siffror din knasboll!")
        gissa()
if __name__ == "__main__":
    gissa()
