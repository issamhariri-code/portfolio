# SQL EmployeeTimeStamps
Issam Adam Hariri
DevOps 25, Databashantering

## Beskrivning
Det här är en liten övning jag gjorde i SQL-kursen för att fortsätta arbeta med WHERE satser, öva på datumfunktioner och filtrering av data som i detta fall var 'In' och 'Out' exempelvis.
Jag skapade en tabell som heter EmployeeTimeStamps som fungerar som ett “passersystem” där man ser när personer stämplar in och ut.

Scriptet börjar med lite testdata där jag lägger in mina INSERT satser så att tabellen kan ha realistiska in och utstämplingar över olika datum med olika anställda.

Sedan genomförde jag dessa uppgifter utifrån datan som finns tillgänglig

1. Lista alla instämplingar  
2. Visa instämplingar för en specifik anställd  
3. Hämta unika EmployeeID som stämplat in  
4. Visa alla utstämplingar  
5. Visa instämplingar efter ett visst datum  
6. Instämplingar före kl 09.00  
7. Alla stämplingar från ett specifikt datum  
8. Instämplingar från en viss plats (MachineName)  
9. Instämplingar under en viss veckodag (t.ex. Friday med DAYNAME())  
10. Utstämplingar på ett specifikt datum  

## SQL Funktioner

### DATE(TimeStamp)

Det här plockar bara ut själva datumet ur en datetime.
Så om värdet är 2023-11-03 08:55:00 -> DATE tar bara 2023-11-03.

Jag använde det när jag behövde filtrera fram stämplingar från ett specifikt datum.

```sql
DATE(TimeStamp) = '2023-11-03';
```

### TIME(TimeStamp)

2023-11-02 08:05:00 -> TIME = 08:05:00.

Jag använde den här när jag skulle hitta instämplingar före kl 09:00, alltså bara jämföra själva tiden. TimeStamp innehåller flera "objekt" som datum och tid. När vi vill bara få fram TID så måste man specifiera det med TIME innan TimeStamp.

```sql
TIME(TimeStamp) < '09:00:00';
```

### DAYNAME(TimeStamp)

DAYNAME tar datumet och gör det till en veckodag:
t.ex. "Monday", "Tuesday", "Friday".

Jag använde den i uppgiften där man skulle visa instämplingar på en viss veckodag.
Först provade jag med "Monday" men fick inget resultat, egentligen spelar det ingen roll men jag gillar
att få data så med Friday fick jag mer data.

```sql
DAYNAME(TimeStamp) = 'Friday';
```
