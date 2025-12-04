import random
from datetime import datetime
from pathlib import Path
import json

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

#                 FÖRKLARING TILL INTERVALL FUNKTION !
# Om attack är > 10 så blir attack ett slumpat tal mellan (attack - varians) och attack
# annars: Alltså om attack nivån på Pokemon inte är högre än 10 så blir 
# skadan ett slumpat tal mellan (attack - varians) (attack + varians)
# Alltså det är helt som vanligt, t.ex har du 8 i attack och varians på 4 kan du slå
# lägst 4 och högst 12. 
    def intervall(self) -> int:
        if self.attack > 10:
            low = self.attack - self.varians
            if low < 1:
                low = 1
            high = self.attack
            return random.randint(low, high -1)
        else:
            low = self.attack - self.varians
            if low < 1:
                low = 1
            high = self.attack + self.varians
            return random.randint(low, high)
        
            
#Slumpar slag mellan högsta och lägsta intervallet, den variabeln kallar vi för varians.
        #högsta = self.attack + self.varians
        #slumpa = random.randint(lägsta, högsta)
        #return slumpa

#Funktion för att undvika att hälsan kan få en negativ siffra vilket jag stötte på flera gånger
#Här säger vi istället att om hälsan(hp) är mindre än 0 så är hp 0.
    def klipp_hp(self) -> None:
        if self.hp < 0:
            self.hp = 0
##Detta är en koll för att se att HP nollställs efter varje strid.
    def is_alive (self) -> bool:
        """Returnerar True om HP är större än 0"""
        return self.hp > 0

    def copy_pokemon(self) -> "Pokemon":
        ny = Pokemon(self.namn, self.attack, self.hp, self.varians)
        ny.max_hp = self.max_hp
        return ny


def lista_pokemon(pokemon_list: list[Pokemon]) -> None:
    for index, p in enumerate(pokemon_list, start=1):
        print(f"{index}. {p.namn} (ATK {p.attack}, HP {p.hp}/{p.max_hp}, VAR {p.varians})")


def lagg_till_pokemon(pokemon_list: list[Pokemon]) -> None:
    try:
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
    except ValueError:
        print("Fel: attack, hp och varians måste vara siffror!")

#Funktion för att ta bort pokemon om ej pokemon finns så printas detta ut
def ta_bort_pokemon(pokemon_list: list[Pokemon]) -> None:
    if not pokemon_list:
        print("Det finns ingen Pokemon att ta bort. ")
        return
#Lagt till try/except fel ifall det är index fel eller syntax fel (int)
    lista_pokemon(pokemon_list)
    svar = input("Skriv numret på en Pokemon att ta bort: ")
    try:
        val = int(svar)

        if val < 1 or val > len(pokemon_list):
            print("Det numret finns inte.")
            return
        index = val - 1
        borttagen = pokemon_list.pop(index)
        print(f"Tog bort följande Pokemon: {borttagen.namn}")
    except ValueError:
        print("Fel, du måste skriva en siffra !")
    except IndexError:
        print("Ogiltigt nummer, ingen Pokemon där.")


def spara_resultat(results: list[dict]) -> None:
    # bestämmer sökväg mappen data och filnamnet matches.json
    data_dir = Path(__file__).parent / "data"
    # Kollar att mappen data existerar 
    data_dir.mkdir(parents=True, exist_ok=True)
    file_path = data_dir / "matches.json"
    with file_path.open('w', encoding='utf-8') as f:
        # skriver ned listan i json format
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Sparade {len(results)} strider till {file_path}")

#Funktion för att visa statistik menyval 6
def visa_statistik(results):
    if not results:
        print("Ingen statistik att visa, spela en strid.")
        return
    vinster = {}
#Om de ej finns statistik att visas så körs först denna 
    for match in results:
        vinnare = match.get("Vinnare") or match.get("vinnare")
        if not vinnare:
            continue
        if vinnare in vinster:
            vinster[vinnare] += 1
        else:
            vinster[vinnare] = 1
#Loop för att registrera vinnar resultat
    print("--STATISTIK--")
    print("Totalt antal matcher:", len(results))
        
    print("Antal vinster per Pokemon:")
    for namn, antal in vinster.items():
        print(f"{namn}: {antal}")
        
#Här påbörjas stridsloopen även lagt till ValueError för att säkerställa att de int
def starta_strid(pokemon_list, results: list[dict]):
    while True:
        lista_pokemon(pokemon_list)
        try:
            val = int(input("Välj en siffra för att välja en Pokemon. "))
        except ValueError:
            print("Fel! Du måste skriva en siffra")
            continue

        if val < 1 or val > len(pokemon_list):
            print("Fel, pröva igen.")
            continue

        index = val - 1
        original_player = pokemon_list[index]
        # välj en motståndare som inte är samma som spelaren
        possible_enemies = [p for i, p in enumerate(pokemon_list) if i != index]
        original_enemy = random.choice(possible_enemies) if possible_enemies else random.choice(pokemon_list)

        player_pokemon = original_player.copy_pokemon()
        enemy_pokemon = original_enemy.copy_pokemon()

        print(f"Du valde {player_pokemon.namn} (Attack: {player_pokemon.attack}, Hälsa: {player_pokemon.hp}, Varians: {player_pokemon.varians})")
        print(f"Motståndaren är: {enemy_pokemon.namn}, (Attack: {enemy_pokemon.attack}, Hälsa: {enemy_pokemon.hp}, Varians: {enemy_pokemon.varians})")

        while player_pokemon.is_alive() and enemy_pokemon.is_alive():
            # spelarens tur
            slumpa_skada = player_pokemon.intervall()
            enemy_pokemon.hp -= slumpa_skada
            enemy_pokemon.klipp_hp()
            print(f"{player_pokemon.namn} slog {enemy_pokemon.namn} med {slumpa_skada} damage points. Hälsa: {enemy_pokemon.hp}/{enemy_pokemon.max_hp}")
            if enemy_pokemon.hp <= 0:
                print(f"{player_pokemon.namn} Vann striden !")
                result = {
                    "Vinnare": player_pokemon.namn,
                    "Förlorare": enemy_pokemon.namn,
                    "tid": datetime.now().isoformat(timespec="seconds"),
                }
                results.append(result)
                break

            # motståndarens tur
            slumpa_skada = enemy_pokemon.intervall()
            player_pokemon.hp -= slumpa_skada
            player_pokemon.klipp_hp()
            print(f"{enemy_pokemon.namn} slog {player_pokemon.namn} med {slumpa_skada} damage points. Hälsa: {player_pokemon.hp}/{player_pokemon.max_hp}")
            if player_pokemon.hp <= 0:
                print(f"{enemy_pokemon.namn} Vann striden !")
                result = {
                    "Vinnare": enemy_pokemon.namn,
                    "Förlorare": player_pokemon.namn,
                    "tid": datetime.now().isoformat(timespec="seconds"),
                }
                results.append(result)
                break

        # Striden är slut här (någon vann). Fråga om användaren vill spela igen.
        question = input("Vill du spela igen? svara med ett (Y / N): ")
        svar = question.strip().lower()
        if svar == "y":
            continue
        else:
            return