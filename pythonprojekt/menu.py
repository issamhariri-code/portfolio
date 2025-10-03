"""Filen innehåller en meny med olika funktioner för spelet"""

"""skriver ut huvudmenyn"""
def print_menu():
    print("1) Lista Pokemon. ")
    print("2) Lägg till Pokemon. ")
    print("3) Ta bort Pokemon. ")
    print("4) Starta strid <--- ")
    print("5) Spara resultat (JSON) ")
    print("6) Läs resultat (JSON) ")
    print("0) Avsluta. ")

def get_choice() -> str:
    meny_val = input("Välj ett av alternativen nedan. ")
    meny_val = meny_val.strip()
    return meny_val