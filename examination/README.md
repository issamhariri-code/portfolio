#Examinationsuppgift
Skapat en README fil för att logga och ha koll på mina uppgifter att göra under examinationsuppgiften.
##Vad programmet gör
Formulär i webbläsaren:
År, månad, dag samt nuvarande kurspris
Användaren skriver in en TICKER eller företagsnamnet exempel:
tsla/TSLA eller TESLA/tesla
Output: 
Sortera: Pris (Close stigande)
Sortera: Pris (Close fallande)
Sortera: %-förändring ((Close–Open)/Open)
Sortera: %-förändring 
Topp 3 vinnare (högst %-förändring)
Topp 3 förlorare (lägst %-förändring)

##Varje rad i resultatet är ett objekt eller dict med.
##EXEMPEL
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "date": "YYYY-MM-DD",
  "open": float,
  "high": float,
  "low": float,
  "close": float,
  "pct_change": float  # kan avrundas i visning, ej i beräkning
}

##Visning av resultat:
Överst: en rad som sammanfattar urvalet:
“Datum: 2025-10-22 • Perspektiv: Sortera %-förändring  • Antal: 5”
Tabell med kolumner:
Ticker | Namn | Öppning | Högsta | Lägsta | Stängning | %-förändring
Vid “Topp 3”:
Antingen visa samma tabell men endast topp 3
eller två korta listor “Vinnare”/“Förlorare” om du vill dela upp dem (valfritt).
(För Programmering 2 räcker en tabell med topp 3.)
Fel/varningar visas överst i resultatet:
“Hittade ingen data för ‘ÅÄÖ’ på valt datum – raden utelämnades.”
“Färre än 3 tickers hade giltiga data …”

Felhantering:
Egen 404 sida om användaren vill ta sig till en endpoint som inte finns.
Om API inte svarar ska man ge ett felmeddelande.
Blandad input: “apple, TSLA, NVDA ” trimma
Okänd input: namnet matchar ingen ticker → lägg felmeddelande, fortsätt med resten.
Delvis fel: om 1 av 5 tickers inte hämtas (404/timeout), visa varning men lista övriga.
Helfel: om 0 giltiga rader → visa tydlig text:
“Inga resultat. Kontrollera datum och tickers.”



##Kriterier
Resultatvyn ska ge olika perspektiv på data

Jag som användare ska kunna få olika data för olika tickers.

Tomma/ogiltiga fält: visar minst ett tydligt felmeddelande i vyn.

Resultatsida: innehåller exakt 24 tidssteg (00:00–23:00) i hh:mm.

404: /något-som-inte-finns returnerar status 404 och visar vår egen 404-mall.

Tester: pytest körs och minst en test i varje testfil passerar.



