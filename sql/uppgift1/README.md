Övningsbeskrivning av MOVIES Tabell
Övningsuppgift Databashantering
Av : Issam Adam Hariri

Listar varje fråga 1-10 och beskriver vad jag gör i förhållande till frågan.

1. Hämtar alla filmer (alla kolumner och rader)

2. Visar filmer som tillhör en specifik genre.
SELECT TITLE och WHERE är viktigast. WHERE talar om vart SQL ska titta, i "Action"

3. Sorterar alla filmer efter Release Year. (Nyast först)
Genom att lägga till en DESC får man högst värde längst upp och sedan faller det ner.
Funkar dock utan att köra DESC, det räcker med bara ORDER BY

4. Uppdaterar rating på en specifik film. Använder UPDATE satsen som vi gjorde i tidigare uppgift
med tabellen "Products". SET (sätter nytt värde), vart = där movieid är 1.

5. Räknar hur många filmer det finns i varje genre.

6. Hämtar endast Titel och Regissör för alla filmer. 

7. Visar filmer som släppts efter ett årtal som jag själv får välja.
WHERE viktigt att få med, annars lätt att tänka python här med jämförelseoperationer.

8. Ökar speltid med 30 minuter för alla filmer i ett visst genre.
Man kan antingen hårdkoda och köra RunTimeMinutes = 200 (exempel) då har man ändrat RunTimeMinutes
för alla filmer i genret 'Action' som jag valde. Dock så var det nämnt att vi ska ÖKA inte ändra
då kör man ganska likt Python. RunTimeMinutes = RunTimeMinutes + 30. Alltså vi har vårt ursprungliga
värde i RunTimeMinutes och nu plussar vi bara på med 30 minuter . 

9. Visar de 5 filmer som har högst rating. LIMIT 5 alltså bara max 5 filmer listade
ORDER BY sätter dom i ordning och DESC gör att högsta värdet är först på listan med fallande värde.

10. Visar titlar på filmer av en specifik regissör jag valde 'Frank Martin'. Enkel kommandon likt Python
Väljer kolumn Title. Från Tabellen Movies. Där Director heter Frank Martin.