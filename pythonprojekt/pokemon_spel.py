import random
import time


# Lista på Pokémon med deras attack och hälsa
pokemon_list = [
    {"name": "Snorlax", "attack": 15, "hp": 50},
    {"name": "Poliwrath", "attack": 12, "hp": 60},
    {"name": "Charmander", "attack": 10, "hp": 40},
    {"name": "Bulbasaur", "attack": 8, "hp": 45},
    {"name": "Pikachu", "attack": 14, "hp": 35}
]

# Funktion för att visa alla tillgängliga Pokémon
def visa_pokemon(pokemon_list):
    print("Här är alla tillgängliga Pokémon:")
    for index, pokemon in enumerate(pokemon_list, 1):
        print(f"{index}. {pokemon['name']}")

# Funktion för att låta användaren välja en Pokémon
def val_av_pokemon(pokemon_list):
    while True:
        try:
            val = int(input("Välj en Pokémon genom att skriva ett nummer (1-5): "))
            if 1 <= val <= len(pokemon_list):
                return pokemon_list[val - 1]
            else:
                print("Ogiltigt val, välj ett nummer mellan 1 och 5.")
        except ValueError:
            print("Felaktigt val. Ange ett nummer.")

# Funktion som hanterar attacken mellan två Pokémon
def attack(pokemon_a, pokemon_b):
    damage = random.randint(1, pokemon_a["attack"])
    pokemon_b["hp"] -= damage
    return damage
#Efter felsökning såg jag att HP(health points) inte nollställs efter varje strid
#För att lösa detta behövde jag "klona" min dict innan stridsumuleringen så att 
#HP nollställs och alla pokemon har fullt liv inför en ny strid.
def klona_pokemon(pokemon_dict):
    ny = {
        "name": pokemon_dict["name"],
        "attack": pokemon_dict["attack"],
        "hp": pokemon_dict["hp"]
    }
    return ny

# Funktion för att simulera en strid mellan två Pokémon
def simulera_strid(pokemon_a, pokemon_b):
    print(f"\nStriden är i gång mellan {pokemon_a['name']} och {pokemon_b['name']}!\n")
    
    while pokemon_a["hp"] > 0 and pokemon_b["hp"] > 0:
        # Pokémon A attackerar Pokémon B
        damage = attack(pokemon_a, pokemon_b)
        print(f"{pokemon_a['name']} attackerar {pokemon_b['name']} och gör {damage} skada! {pokemon_b['name']} har {max(pokemon_b['hp'], 0)} HP kvar.")
        
        if pokemon_b["hp"] <= 0:
            break

        # Pokémon B attackerar Pokémon A
        damage = attack(pokemon_b, pokemon_a)
        print(f"{pokemon_b['name']} attackerar {pokemon_a['name']} och gör {damage} skada! {pokemon_a['name']} har {max(pokemon_a['hp'], 0)} HP kvar.\n")

    if pokemon_a["hp"] > 0:
        print(f"{pokemon_a['name']} vinner striden!\n")
        if pokemon_a['name'] == "Snorlax":
            print("Snorlax utvecklas till Skylax!\n")
    else:
        print(f"{pokemon_b['name']} vinner striden!\n")

# Funktion som hanterar en individuell strid
def spela_strid():
    print("Välkommen till Pokémon-striden!")
    print("Välj din Pokemon: ")
    visa_pokemon(pokemon_list)

    # Spelaren väljer sin Pokémon
    spelarens_pokemon = val_av_pokemon(pokemon_list)
    print()
    print(f"\nDu har valt: {spelarens_pokemon['name']}!\n")
    input("Tryck Enter för att välja motståndare !")
    
    # Spelaren väljer en motståndare
    print()
    print("\nVälj en motståndare:")
    visa_pokemon(pokemon_list)
    motstandares_pokemon = val_av_pokemon(pokemon_list)
    while motstandares_pokemon == spelarens_pokemon:
        print("Du kan inte välja samma Pokémon som motståndare!")
        motstandares_pokemon = val_av_pokemon(pokemon_list)

    spelarens_kopia = klona_pokemon(spelarens_pokemon)
    motstandares_kopia = klona_pokemon(motstandares_pokemon)

    print()
    print(spelarens_pokemon["name"], "vs", motstandares_pokemon["name"])
    input("Tryck Enter för att starta striden !")

    print()
    print("===========================")
    print("       STRID STARTAR       ")
    print("===========================")
    print()

    for n in [3, 2, 1]:
        print(n, flush=True)
        time.sleep(1)
    
    print("GO !")
    time.sleep(0.5)


    # Simulera striden
    simulera_strid(spelarens_kopia, motstandares_kopia)

# Funktion för att hantera hela spel-loopen
# Ändra så att simuleringen inte startar förrän du anropat striden
#Ändra så att Frågan om du vill spela igen kommer efter print och paus
#Ändra så att du måste fortsätta innan frågan om du vill spela igen kommer med input
def spel_loop():
    while True:
        try:
            spela_strid()
            input("Tryck Enter för att fortsätta")
            spela_igen = input("\nVill du spela en strid till? (ja/nej): ").lower()
            if spela_igen != "ja":
                print("Tack för att du spelade! Hej då!")
                break
        except Exception as e:
            print(f"Något gick fel: {e}. Försök igen.")

# Huvudfunktion för att starta spelet
if __name__ == "__main__":
    spel_loop()