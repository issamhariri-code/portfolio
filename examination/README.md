#Examinationsuppgift
Skapat en README fil för att logga och ha koll på mina uppgifter att göra under examinationsuppgiften.
##Vad programmet gör
Formulär i webbläsaren:
År,Månad,Dag,Prisklass. (Enligt API)
Användaren ska fylla i sökformuläret och sedan trycka på "sök".

Validering av datum:
Tidigast datum:
2022 - 11 - 01
Senast:
Imorgon, (max +1dag framåt)
Ogiltiga datum:
31/02, samt tomma fält ska ge felmeddelanden i samma formulärvy.
När validering är OK, hämtas API för vald dag samt prisklass, svaret struktureras per timme.

Visning av resultat:
En enkel lista/tabell med alla timmar 00.00 - 23.00
tidsformat hh:mm 
Tydlig rubrik med datum och prisklass

Felhantering:
Egen 404 sida om användaren vill ta sig till en endpoint som inte finns.
Om API inte svarar ska man ge ett felmeddelande.

##Vad programmet ska göra för användaren 
Som användare vill jag få ett tydligt fel om datumet är före 2022-11-01.
Som användare vill jag få ett tydligt fel om datumet är längre fram än i morgon.
Som användare vill jag se timmarna i formatet hh:mm.
Som användare vill jag mötas av en trevlig 404-sida om jag skriver fel adress.

##Kriterier
Datumgräns bakåt: 2022-10-31 → underkänns, 2022-11-01 → godkänns.

Datumgräns framåt: dagens datum + 2 dagar → underkänns; dagens datum + 1 dag (i morgon) → godkänns.

Tomma/ogiltiga fält: visar minst ett tydligt felmeddelande i vyn.

Resultatsida: innehåller exakt 24 tidssteg (00:00–23:00) i hh:mm.

404: /något-som-inte-finns returnerar status 404 och visar vår egen 404-mall.

Tester: pytest körs och minst en test i varje testfil passerar.



