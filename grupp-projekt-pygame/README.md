# MINIL-tech – Grupprojekt i Pygame

Ett 2D-plattformsspel som vi utvecklade som grupparbete med Scrum, Python och
Pygame. Spelaren styr en karaktär genom olika banor, hoppar mellan plattformar,
samlar poäng och möter fiender och en boss.

Min roll i gruppen var att programmera spelkaraktärens funktioner. Här finns
hela gruppens spel tillsammans med dokumentationen från vårt Scrum-arbete.

## Mitt arbete med spelkaraktären

Jag ansvarade för att konfigurera och programmera karaktären, från val av
sprite och storlek till hur figuren rör sig och reagerar på spelarens input.
Det innefattade bland annat:

- Rörelse åt vänster och höger med tangentbordet.
- Hopp, gravitation och stöd för dubbelhopp på senare banor.
- Att ducka och anpassa kollisionsytan efter rörelsen.
- Val och skalning av sprites för att stå stilla, gå, hoppa och ducka.
- Växling mellan gångbilder och att vända figuren efter rörelseriktningen.
- Kollisioner och landning på plattformar.

Spelarlogiken finns i [player.py](game/src/player.py). Där hanteras bland annat
hastighet, hopp, riktning och vilken bild som ska visas. Tangenttryck för hopp
kopplas till spelaren från huvudloopen i [main.py](game/src/main.py).

Rörelse, sprite och kollisionsyta behövde fungera tillsammans. När figuren
landade på en plattform skulle det både fungera i koden och se rätt ut på
skärmen. Det var en viktig del av mitt arbete med karaktären.

## Spelets funktioner

Det här är funktioner i gruppens gemensamma spel:

- Tre banor med olika miljöer och plattformar.
- Karaktär med gånganimationer, hopp, dubbelhopp och möjlighet att ducka.
- Samlarobjekt, poäng, liv och en hatt som power-up.
- Fiender och en boss med egna attacker.
- Huvudmeny, banval, pausmeny och möjlighet att starta om via menyn.
- Musik, ljudeffekter och separata volyminställningar.
- Resultat och high score som sparas lokalt i [game/data/scores.json](game/data/scores.json).

## Testa spelet

Spelet körs lokalt i ett Pygame-fönster. Du behöver Git, Python 3.11 eller
senare och en miljö som kan visa grafiska fönster och spela ljud.
Pythonberoendet är `pygame==2.6.1` och finns i [requirements.txt](requirements.txt).

### Windows – PowerShell

Klona portfolion och gå till projektmappen:

```powershell
git clone https://github.com/issamhariri-code/portfolio.git
cd portfolio/grupp-projekt-pygame
```

Skapa en egen virtuell miljö och installera beroendet:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Starta spelet:

```powershell
cd game/src
..\..\.venv\Scripts\python.exe main.py
```

### Linux och macOS

```bash
git clone https://github.com/issamhariri-code/portfolio.git
cd portfolio/grupp-projekt-pygame
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cd game/src
../../.venv/bin/python main.py
```

Om repot redan är klonat börjar du i din befintliga mapp
`portfolio/grupp-projekt-pygame` och skapar miljön där.
Kommandona använder miljöns Python direkt, så den behöver inte aktiveras separat.

När fönstret öppnas kan du starta spelet eller välja bana från menyn.
Fönstret är inställt på 1920 × 1080. Vid körning genom WSL behövs stöd för
grafiska program och ljud, exempelvis WSLg.

### Kontroller

| Funktion | Tangent |
| --- | --- |
| Gå åt vänster | A eller vänsterpil |
| Gå åt höger | D eller högerpil |
| Hoppa | Mellanslag, W eller uppåtpil |
| Dubbelhoppa när banan tillåter det | Tryck hopptangenten igen i luften |
| Ducka | S eller nedåtpil |
| Pausa eller återuppta | Esc |
| Använd menyerna | Mus |

Börja gärna med att gå, hoppa och ducka för att testa karaktärens rörelser.
På senare banor finns dubbelhopp, fler fiender och bossen.

## Scrum och samarbete

Arbetet delades upp i gruppen med backlogg, sprintuppgifter och daily standups.
Mitt fokus var spelkaraktären och hur den fungerade ihop med banorna och
övriga delar av spelet.

Dokumentationen finns kvar här:

- [Produktvision](scrum/product_vision.md)
- [Produktbacklogg](scrum/product_backlog.md)
- [Sprintbacklogg](sprint_backlog.md)
- [Daily standups](scrum/daily-standups/)
- [Teknisk översikt](scrum/tech_overview.md)

## Hitta i projektet

```text
grupp-projekt-pygame/
├── game/
│   ├── src/           # Spelkod, bland annat main.py och player.py
│   ├── assets/        # Sprites, bakgrunder, plattformar och ljud
│   └── data/          # Sparade resultat och mapp för ban-data
├── scrum/             # Planering och dokumentation från grupparbetet
├── docs/              # Bland annat guide för pull requests
├── sprint_backlog.md
├── requirements.txt
└── README.md
```
