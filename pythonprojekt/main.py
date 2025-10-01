from pokemon import Pokemon
import random
from menu import print_menu, get_choice
from datetime import datetime
from pathlib import Path
import json

results: list[dict] = []

pokemon1 = Pokemon("Pikachu", 12, 60, 8)
pokemon2 = Pokemon("Bulbasaur", 8, 70, 6)
pokemon3 = Pokemon("Snorlax", 6, 80, 4)
pokemon4 = Pokemon("Charmander", 13, 55, 8)

pokemon_list = [pokemon1, pokemon2, pokemon3, pokemon4]

def starta_strid(pokemon_list):
    while True:
        lista_pokemon(pokemon_list)
        val = int(input("Välj en siffra för att välja en Pokemon. "))
        if val < 1 or val > len(pokemon_list):
            print("Fel, pröva igen.")
            return
        index = val - 1
        original_player = pokemon_list[index]
        original_enemy = random.choice(pokemon_list)

        player_pokemon = original_player.copy_pokemon()
        enemy_pokemon  = original_enemy.copy_pokemon()

        print(f"Du valde {player_pokemon.namn} (Attack: {player_pokemon.attack}, Hälsa: {player_pokemon.hp}, Varians: {player_pokemon.varians})")
        print(f"Motståndaren är: {enemy_pokemon.namn}, (Attack: {enemy_pokemon.attack}, Hälsa: {enemy_pokemon.hp}, Varians: {enemy_pokemon.varians})")


        
        while player_pokemon.is_alive() and enemy_pokemon.is_alive():
            #spelarens tur
            slumpa_skada = player_pokemon.intervall()
            enemy_pokemon.hp -= slumpa_skada
            enemy_pokemon.klipp_hp()
            print(f"{player_pokemon.namn} slog {enemy_pokemon.namn} för {slumpa_skada} HP kvar: {enemy_pokemon.hp}/{enemy_pokemon.max_hp}")
            if enemy_pokemon.hp == 0:
                print(f"{player_pokemon.namn} Vann striden !")
                break
            #motståndarens tur
            slumpa_skada = enemy_pokemon.intervall()
            player_pokemon.hp -= slumpa_skada
            player_pokemon.klipp_hp()
            print(f"{enemy_pokemon.namn} slog {player_pokemon.namn} för {slumpa_skada} HP kvar: {player_pokemon.hp}/{player_pokemon.max_hp}")
            if player_pokemon.hp == 0:
                print(f"{enemy_pokemon.namn} Vann striden !")
                break

        # Striden är slut här (någon vann). Fråga om användaren vill spela igen.
        question = input("Vill du spela igen? svara med ett (Y / N): ")
        svar = question.strip().lower()
        if svar == "y":
            continue
        else:
            return

def meny_loop():
    while True:
        print_menu()
        val = get_choice()
        if val == "1":
            lista_pokemon(pokemon_list)
        elif val == "2":
            lagg_till_pokemon(pokemon_list)
        elif val == "3":
            ta_bort_pokemon(pokemon_list)
        elif val == "4":
            starta_strid(pokemon_list)
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
    if not pokemon_list:
        print("Det finns ingen Pokemon att ta bort. ")
        return

    lista_pokemon(pokemon_list)
    svar = input("Skriv numret på en Pokemon att ta bort: ")
    val = int(svar)

    if val < 1 or val > len(pokemon_list):
        print("Det numret finns inte.")
        return
    
    index = val - 1
    borttagen = pokemon_list.pop(index)
    print(f"Tog bort följande Pokemon: {borttagen.namn}")


if __name__ == "__main__":
    meny_loop()