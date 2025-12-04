from pokemon import (
    Pokemon,
    lista_pokemon,
    lagg_till_pokemon,
    ta_bort_pokemon,
    starta_strid,
    spara_resultat,
    visa_statistik,
)


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

def meny_loop(pokemon_list: list = None, results: list[dict] = None):
    # Skapa default-data om inga argument skickas (så main.py kan vara minimal)
    if results is None:
        results = []
    if pokemon_list is None:
        pokemon1 = Pokemon("Pikachu", 12, 60, 8)
        pokemon2 = Pokemon("Bulbasaur", 8, 70, 6)
        pokemon3 = Pokemon("Snorlax", 6, 80, 4)
        pokemon4 = Pokemon("Charmander", 13, 55, 8)
        pokemon_list = [pokemon1, pokemon2, pokemon3, pokemon4]

    while True:
        print_menu()
        val = get_choice()
        if val == "1":
            lista_pokemon(pokemon_list)
            # La till en paus efter felsökning, menyn loopades efter val 1,5,6 
            # vilket gör att man måste förstora terminalen för att se output.
            input("Tryck (Enter) för att komma tillbaka till Menyn") #paus input
        elif val == "2":
            lagg_till_pokemon(pokemon_list)
        elif val == "3":
            ta_bort_pokemon(pokemon_list)
        elif val == "4":
            starta_strid(pokemon_list, results)
        elif val == "5":
            spara_resultat(results)
            input("Tryck (Enter) för att komma tillbaka till Menyn") #paus input
        elif val == "6":
            visa_statistik(results)
            input("Tryck (Enter) för att komma tillbaka till Menyn") #paus input
        elif val == "0":
            print("Programmet avslutades..")
            break