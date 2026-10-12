#!/bin/bash

# Skript för att skapa Daily Stand-up mall automatiskt
# Skapad för Minil-Tech projekt - Scrum dokumentation

# Hitta projekt-roten automatiskt (git repository root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel 2>/dev/null)"

# Om inte i en git repo, använd skriptets plats som referens
if [ -z "$PROJECT_DIR" ]; then
    # Anta att skriptet är i scrum/daily-standups eller liknande
    PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

SCRUM_DIR="$PROJECT_DIR/scrum/daily-standups"
mkdir -p "$SCRUM_DIR"

# Hämta dagens datum
TODAY=$(date +%d%m)  # Format: DDMM (t.ex. 0212)
FULL_DATE=$(date +"%d %B %Y")  # Format: 02 December 2024

# Filnamn
FILENAME="$SCRUM_DIR/daily${TODAY}.md"
IMAGE_NAME="daily${TODAY}.png"

# Kolla om filen redan finns
if [ -f "$FILENAME" ]; then
    echo "Daily stand-up för $FULL_DATE finns redan: $FILENAME"
    echo "Skippar för att inte skriva över."
    exit 0
fi

# Skapa filen med mall
cat > "$FILENAME" << 'EOF'
# Daily Stand-up - DATE_PLACEHOLDER

**Tid:** 08:15
**Plats:** Discord

## Närvarande
- Ikaros
- Love
- Markus
- Nila
- Issam

## Frånvarande
Ingen

---

### Ikaros
**Vad gjorde jag igår/senast?**
- 

**Vad ska jag göra idag?**
- 

**Några hinder?**
- Inga hinder

---

### Love
**Vad gjorde jag igår/senast?**
- 

**Vad ska jag göra idag?**
- 

**Några hinder?**
- Inga hinder

---

### Markus
**Vad gjorde jag igår/senast?**
- 

**Vad ska jag göra idag?**
- 

**Några hinder?**
- Inga hinder

---

### Nila
**Vad gjorde jag igår/senast?**
- 

**Vad ska jag göra idag?**
- 

**Några hinder?**
- Inga hinder

---

### Issam
**Vad gjorde jag igår/senast?**
- 

**Vad ska jag göra idag?**
- 

**Några hinder?**
- Inga hinder

---

## Scrum Board vid mötets slut
![Scrum Board](./IMAGE_PLACEHOLDER)

## Anteckningar
- 
- Nästa Daily: NEXT_DATE_PLACEHOLDER 08:15 på Discord
EOF

# Ersätt placeholders med faktiska datum
sed -i "s/^# Daily Stand-up - DATE_PLACEHOLDER/# Daily Stand-up - $FULL_DATE/" "$FILENAME"
sed -i "s/IMAGE_PLACEHOLDER/$IMAGE_NAME/g" "$FILENAME" # Här ersätts bildnamn

# Beräkna morgondagens datum för "Nästa Daily"
TOMORROW=$(date -d "+1 day" +"%d %B")
sed -i "s/NEXT_DATE_PLACEHOLDER/$TOMORROW/g" "$FILENAME" # Här ersätts nästa datum

echo "Skapade Daily Stand-up mall: $FILENAME" # loggmeddelande
echo "Kom ihåg att ta skärmdump och ersätt Scrum bild: $IMAGE_NAME" # påminnelse om bild