Innehåll i beginner.sql

1. Skapa tabell
Jag skapar tabellen Products med tre kolumner:

ProductID (PRIMARY KEY, unikt ID)

ProductName (produktens namn)

Price (pris med två decimaler)

2. Lägga till data (INSERT)
Jag lägger in tre produkter med sina ID, namn och priser.

3. Hämta data (SELECT)
Jag visar hela tabellen och testar att hämta enskilda kolumner, t.ex. bara priset.

4. Filtrera data (WHERE)
Jag väljer ut produkter som kostar mer än 50.

5. Sortera data (ORDER BY)
Jag sorterar produkterna efter pris i fallande ordning descending där dyrast är först.

6. Räkna rader (COUNT)
Jag räknar hur många produkter tabellen innehåller.

7. Uppdatera data (UPDATE)
Jag höjer priset på en produkt med ett specifikt ProductID.

8. Ta bort data (DELETE)
Jag tar bort en rad från tabellen genom att använda den unika ProductID.
Varför jag använder ProductID för att ta bort data är för att flera "objekt" kan ha
samma ProductName och samma Price i SQL kommer allt raderas om jag specifierar Productname
eller Price vilket kan göra strul i databasen. Väljer man ProductID så är det mer precision
du vet exakt vilken rad som försvinner för varje ID är unikt.

9. Ändra tabellens struktur (ALTER TABLE)
Jag lägger till en ny kolumn Stock för att kunna spåra lagersaldo.