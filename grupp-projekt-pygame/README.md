# MINIL-tech

Minil-tech är ett 2D-plattformsspel där spelaren tar sig igenom korta, tydliga banor med gradvis ökande svårighetsgrad.

Spelet ska växa steg för steg med nya världar, fiendetyper och rörelseförmåner utan att tappa en enkel och lätt att förstå spelkänsla.

Målet är att skapa ett spel som spelare vill återvända till eftersom det alltid finns ett nytt litet steg att ta och en ny utmaning att klara.

---

## Teknisk överblick

- **Språk:** Python 3  
- **Bibliotek:** Pygame  
- **Körs som:** Desktop-spel med Pygame-fönster  
- **Nuvarande MVP:**
  - Röd spelare (rektangel) som kan röra sig med WASD/piltangenter
  - Hopp med gravitation och marknivå
  - Enkel bakgrundsfärg och game loop som kör i 60 FPS

---

## Kom igång

### 1. Förutsättningar

- Python 3.11(och upåt) installerat
- Git installerat

### 2. Klona repo och gå till mappen

```bash
git clone <REPO-URL>
cd pr-projektuppgift-d5-minil-tech
```

## 3.Skapa och aktivera virtuell miljö

Windows PowerShell:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
``` 

### 4. Installera beroenden

```bash
pip install -r requirements.txt
``` 

### 5. Starta spelet

```bash
cd game/src
python main.py
```
Spelet öppnas i ett grönt fönster med en röd spelare som du kan styra med piltangenterna eller WASD och hoppa med `space`.

---

## Projektstruktur

```

├─ game/
│  ├─ src/
│  │  ├─ main.py        # Startpunkt, initierar Pygame och kör game loop
│  │  ├─ player.py      # Spelarlogik: rörelse, hopp, gravitation
│  │  ├─ function.py    # (förberedd för framtida hjälpfunktioner)
│  │  ├─ config.py      # (förberedd för framtida konstanter/inställningar)
│  │  └─ tests/         # Tester för spelets moduler
│  ├─ assets/
│  │  ├─ sprites/       # Grafiska resurser (spelare, fiender, objekt)
│  │  ├─ tilesets/      # Tiles till banor
│  │  ├─ maps/          # Kartor/banor
│  │  └─ sounds/        # Musik och ljudeffekter
│  └─ data/
│     └─ levels/        # Ban-data
├─ scrum/               # Scrum-dokumentation och projektstyrning
│  ├─ product_vision.md # Produktvision
│  ├─ product_backlog.md# User stories / produktbacklogg
│  ├─ sprint_backlog.md # Sprint 1–4, tekniska tasks
│  ├─ daily-standups/   # Loggar för daily standups
│  └─ tech_overview.md  # Tekniskt diagram och arkitekturbeskrivning
├─ docs/                # Övrig dokumentation (t.ex. PR-guide)
├─ requirements.txt     # Pythonberoenden (bl.a. pygame)
└─ README.md            # Den här filen

```

---

## Scrum & arbetssätt

Projektet följer Scrum enligt kursens riktlinjer:
- Produktvision: `scrum/product_vision.md`
- Produktbacklogg: `scrum/product_backlog.md`
- Sprint Backlog: `scrum/sprint_backlog.md`
- Daily Standups: Markdown + skärmdump i `scrum/daily-standups/`
- Teknisk översikt: `scrum/tech_overview.md`

---

## Git & Pull Request

- All utveckling sker i feature-brancher från `main`.
- Branch-namn:
    - `feat/...` för nya funktioner i spelet
    - `fix/...` för buggar
    - `docs/...` för dokumentation
- Commit meddelanden följer Conventional Commits:
    - `feat: lägg till ny fiendetyp`
    - `fix: åtgärda krasch vid hopp`
    - `docs: lägg till installationsinstruktioner i README`
- Alla ändringar går via Pull Request:
    - Minst två godkännanden krävs innan merge.
    - `main` är skyddad från direkta pushar.