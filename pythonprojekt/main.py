from pokemon import Pokemon
import random

pokemon1 = Pokemon("Pikachu", 12, 60, 8)
pokemon2 = Pokemon("Bulbasaur", 8, 70, 6)
pokemon3 = Pokemon("Snorlax", 6, 80, 4)
pokemon4 = Pokemon("Charmander", 13, 55, 8)

pokemon_list = [pokemon1, pokemon2, pokemon3, pokemon4]

for index, pokemon in enumerate(pokemon_list):
    print(f"{index+1}. {pokemon.namn} - Attack: {pokemon.attack} Hälsa: {pokemon.hp}/{pokemon.max_hp} Varians: {pokemon.varians}")

val = int(input("Skriv ett tal mellan 1 - 4 för att välja Pokemon "))
index = val - 1

random_pokemon = random.choice(pokemon_list)
copy_pokemon = Pokemon(random_pokemon.namn, 
                       random_pokemon.attack, 
                       random_pokemon.hp,
                       random_pokemon.varians)
copy_pokemon.max_hp = random_pokemon.max_hp

player_pokemon = pokemon_list[index]
print(f"Du valde: {player_pokemon.namn}\n(Attack: {player_pokemon.attack}, Hälsa: {player_pokemon.hp} Varians: {pokemon.varians})")
print(f"Motståndaren är: {random_pokemon}\n(Attack: {random_pokemon.attack}, Hälsa: {random_pokemon.hp}) Varians: {pokemon.varians})")

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