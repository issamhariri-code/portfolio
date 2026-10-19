# Guide för Pull Requests

Den här guiden förklarar hur du bidrar med kod till projektet genom att använda branches och pull requests.

## Översikt

Vår `main`-branch är skyddad, vilket betyder:
- Du kan inte pusha direkt till `main`
- Alla ändringar måste gå genom en pull request
- Minst 2 av oss måste granska och godkänna din PR innan den kan mergas

## Steg-för-Steg Arbetsflöde

### 1. Se till att du är på Main och Uppdaterad

```bash
# Byt till main-branchen
git checkout main

# Hämta de senaste ändringarna från GitHub
git pull origin main
```

### 2. Skapa en Ny Branch för ditt Arbete

Skapa alltid en ny branch för varje funktion eller uppgift:

```bash
# Skapa och byt till en ny branch
git checkout -b feature/ditt-funktionsnamn

# Exempel:
# git checkout -b feature/lagg-till-spelar-rorelser
# git checkout -b bugfix/fixa-kollisions-detektion
# git checkout -b docs/uppdatera-readme
```

**Namnkonventioner för branches:**
- `feature/` - för nya funktioner
- `bugfix/` - för buggfixar
- `docs/` - för dokumentation
- Använd beskrivande namn med bindestreck

### 3. Gör dina Ändringar

Arbeta med din kod som vanligt. Redigera, skapa eller ta bort filer efter behov.

### 4. Kolla Vad du har Ändrat

```bash
# Se vilka filer som har ändrats
git status

# Se de faktiska ändringarna i detalj
git diff
```

### 5. Stagea dina Ändringar

Lägg till filerna du vill commita:

```bash
# Lägg till specifika filer
git add fil1.py fil2.py

# Eller lägg till alla ändrade filer
git add .
```

### 6. Committa dina Ändringar

Spara dina ändringar med ett beskrivande meddelande:

```bash
git commit -m "feat: Lägg till spelarens tangentstyrning"
```

**Bra commit-meddelanden:**
- "feat: Lägg till spelarsprite och rörelselogik"
- "fix: Fixa bugg i kollisionsdetektion"
- "docs: Uppdatera README med setup-instruktioner"

**Dåliga commit-meddelanden:**
- "uppdatering"
- "fixade grejer"
- "asdfgh"

### 7. Pusha din Branch till GitHub

```bash
# Pusha din branch för första gången
git push -u origin feature/ditt-funktionsnamn

# Efter första pushen kan du bara använda
git push
```

### 8. Skapa en Pull Request på GitHub

1. Gå till repositoryt på GitHub
2. Du kommer se ett meddelande som "Your branch had recent pushes" med en knapp **"Compare & pull request"** - klicka på den
   - Eller gå till fliken "Pull requests" och klicka **"New pull request"**
3. Se till att base branch är `main` och compare branch är din feature branch
4. Fyll i pull request-formuläret:
   - **Title**: Kort beskrivning av vad du gjorde
   - **Description**: Förklara vilka ändringar du gjorde och varför
     - Vilken funktion lade du till?
     - Vilken bugg fixade du?
     - Hur kan granskare testa det?
5. Klicka **"Create pull request"**

### 9. Begär Granskningar

1. På höger sida av din PR, hitta "Reviewers"
2. Vänta tills minst 2 av oss har granskat din kod och upplys oss via SMS eller Discord om vi ej skulle se notisen.
3. Vänta på vår feedback

### 10. Svara på Granskningskommentarer

Granskare kan:
- Godkänna din PR
- Begära ändringar
- Lämna kommentarer eller frågor

Om ändringar begärs:

```bash
# Gör ändringarna i din branch
# Stagea och committa dem
git add .
git commit -m "fix: Åtgärda feedback från granskning"

# Pusha uppdateringarna
git push
```

PR:en kommer automatiskt uppdateras med dina nya commits.

### 11. Merga din PR

När du har minst 2 godkännanden:
1. Gå till din PR på GitHub
2. Klicka **"Merge pull request"**
3. Klicka **"Confirm merge"**
4. Ta bort din branch (GitHub kommer erbjuda detta alternativ)

### 12. Städa Upp Lokalt

Efter mergning, städa upp dina lokala branches:

```bash
# Byt tillbaka till main
git checkout main

# Hämta de senaste ändringarna (inklusive din mergade kod)
git pull origin main

# Ta bort din lokala branch
git branch -d feature/ditt-funktionsnamn
```

## Vanliga Scenarion

### Du Behöver Uppdatera din Branch med Senaste Main

Om `main` har uppdaterats medan du arbetade:

```bash
# Medan du är på din feature branch
git checkout main
git pull origin main
git checkout feature/ditt-funktionsnamn
git merge main
```

Eller använd rebase för en renare historik:

```bash
git checkout main
git pull origin main
git checkout feature/ditt-funktionsnamn
git rebase main
```

### Du Gjorde ett Misstag i ditt Commit-Meddelande

Om du inte har pushat än:

```bash
git commit --amend -m "Korrigerat commit-meddelande"
```

Om du redan har pushat, gör bara en ny commit med fixarna.

### Du Vill Se Alla Branches

```bash
# Lokala branches
git branch

# Remote branches
git branch -r

# Alla branches
git branch -a
```

## Snabbreferens

```bash
# Starta nytt arbete
git checkout main
git pull origin main
git checkout -b feature/min-funktion

# Spara ditt arbete
git add .
git commit -m "Beskrivning av ändringar"
git push -u origin feature/min-funktion

# Efter PR är mergad
git checkout main
git pull origin main
git branch -d feature/min-funktion
```

## Tips

- Committa ofta med tydliga meddelanden
- Håll dina branches fokuserade på en funktion/fix
- Pulla från main regelbundet för att undvika konflikter
- Testa din kod innan du skapar en PR
- Tvinga inte pusha till delade branches

## Få Hjälp

Om du stöter på problem:
1. Kolla `git status` för att se vilket tillstånd du är i
2. Fråga en teammedlem om hjälp
3. Använd `git log` för att se senaste commits
4. Använd `git branch` för att se vilken branch du är på

## Regler för Skyddad Main Branch

Kom ihåg:
- Inga direkta pushes till `main`
- Inga force pushes (`git push --force`)
- Måste ha 2 godkännanden innan mergning
- Alla tester måste passera (om vi lägger till CI/CD senare)
