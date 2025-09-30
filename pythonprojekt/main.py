from pokemon import Pokemon
import random
from menu import print_menu, get_choice

pokemon1 = Pokemon("Pikachu", 12, 60, 8)
pokemon2 = Pokemon("Bulbasaur", 8, 70, 6)
pokemon3 = Pokemon("Snorlax", 6, 80, 4)
pokemon4 = Pokemon("Charmander", 13, 55, 8)

pokemon_list = [pokemon1, pokemon2, pokemon3, pokemon4]

def starta_strid(pokemon_list):
    val = int(input("Skriv ett tal mellan 1 - 4 för att välja Pokemon "))
    index = val - 1

    random_pokemon = random.choice(pokemon_list)
    copy_pokemon = Pokemon(random_pokemon.namn, 
                        random_pokemon.attack, 
                        random_pokemon.hp,
                        random_pokemon.varians)
    copy_pokemon.max_hp = random_pokemon.max_hp

    player_pokemon = pokemon_list[index]
    print(f"Du valde: {player_pokemon.namn}\n(Attack: {player_pokemon.attack}, Hälsa: {player_pokemon.hp} Varians: {Pokemon.varians})")
    print(f"Motståndaren är: {random_pokemon}\n(Attack: {random_pokemon.attack}, Hälsa: {random_pokemon.hp}) Varians: {Pokemon.varians})")

    while (player_pokemon) and (random_pokemon):

        """Användaren (spelaren som spelar)"""
        skada = player_pokemon.intervall()
        random_pokemon.hp = random_pokemon.hp - skada
        random_pokemon.klipp_hp()
        print(f"{player_pokemon} slog {random_pokemon} för {skada}. HP kvar: {random_pokemon.hp}")

        if (random_pokemon.hp <= 0):
            print(f"{player_pokemon} Vann striden!")
            break

        """ Motståndaren som spelar (datorn)"""
        skada = random_pokemon.intervall()
        player_pokemon.hp = player_pokemon.hp - skada
        player_pokemon.klipp_hp()
        print(f"{random_pokemon} slog {player_pokemon} för {skada}. HP kvar: {player_pokemon.hp}")

        if (player_pokemon.hp <= 0):
            print(f"{random_pokemon} Vann striden!")
            break


def meny_loop():
    while True:
        print_menu()
        val = get_choice()
        if val == "1":
            lista_pokemon(pokemon_list)
        elif val == "2":
            lagg_till_pokemon(pokemon_list)
        elif val == "3":
            print("Ta bort Pokemon")
        elif val == "4":
            print("Starta en strid. ")
        elif val == "5":
            print("Spara resultat (JSON)")
        elif val == "6":
            print("Visa statistik (JSON)")
        elif val == "0":
            print("Avslutar programmet")
            break

def lista_pokemon(pokemon_list):
    for index, p in enumerate(pokemon_list, start=1):
        print(f"{index}. {p.namn} (ATK {p.attack}, HP {p.hp}/{p.max_hp}, VAR {p.varians})")

def lagg_till_pokemon(pokemon_list: list[Pokemon]) -> None:
    svar = input("Välj ett namn på din Pokemon. ")
    namn = svar
    svar = input("Välj attack t.ex 8. Välj ett tal mellan: (0 - 13)")
    attack = int(svar)
    svar = input("Välj HP (Hälsa) t.ex 60. Välj ett tal mellan (50-80)")
    hp = int(svar)
    svar = input("Välj Varians, ju högre attack desto högre varians väljer du,\nju lägre attack desto lägre varians.")
    varians = int(svar)

    ny_pokemon = Pokemon(namn, attack, hp, varians)
    pokemon_list.append(ny_pokemon)
    print(f"{ny_pokemon.namn} (ATK {ny_pokemon.attack}, HP {ny_pokemon.hp}, VAR {ny_pokemon.varians}) lades till!")

def ta_bort_pokemon(pokemon_list: list[Pokemon]) -> None:
    lista_pokemon(pokemon_list)
    if lista_pokemon is not True:
        print("Inga Pokemon att ta bort")
        return




if __name__ == "__main__":
    meny_loop()