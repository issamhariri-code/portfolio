import sqlite3
import os

# Placera databasen i samma mapp som modulen så samma fil används oavsett CWD
DB_PATH = os.path.join(os.path.dirname(__file__), 'kortspel.db')


def skapa_databas(): #Funktion som skapar databas om den inte redan finns.
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    #Skapar en tabell för stats som visar spelarens och datorns kort och vinnare.
    cur.execute("""CREATE TABLE IF NOT EXISTS stats (
                spelares_kort text,
                datorns_kort text,
                vinnare text)
                """)

    con.commit() #Sparar ändringar
    con.close() #Stänger koppling


def spara_resultat(spelares_kort, datorns_kort, vinnare): #Funktion som sparar resultat
    con = sqlite3.connect(DB_PATH) #Ansluter till kortspel.db
    cur = con.cursor()
    cur.execute(
        "INSERT INTO stats (spelares_kort, datorns_kort, vinnare) VALUES (?, ?, ?)",  #Lägger till ny rad 
        (spelares_kort, datorns_kort, vinnare)
    )

    con.commit() #Sparar ändringar
    con.close() #Stänger kopplingen
    # End of spara_resultat

def visa_statistik():
    con = sqlite3.connect(DB_PATH)#Anslutar till kortspel.db
    cur = con.cursor()
    res = cur.execute(
        "SELECT vinnare, COUNT(*) FROM stats GROUP BY vinnare"  #Hämtar vinnare och räknar hur många gånger de kommer upp i vinnare
    )

    for rad in res.fetchall(): #Hämtar och går igenom alla rader
        vinnare = rad[0]
        antal = rad[1]
        print(f"{vinnare}: {antal}: ") #Skriver ut resultatet


def hamta_senaste(n: int = 10):
    """Returnerar de senaste n raderna som tuples (rowid, spelares_kort, datorns_kort, vinnare)."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    rows = list(cur.execute(
        'SELECT rowid, spelares_kort, datorns_kort, vinnare FROM stats ORDER BY rowid DESC LIMIT ?', (n,)
    ))
    con.close()
    return rows


if __name__ == '__main__':
    # Snabb kontroll när modulen körs direkt
    print('Database path:', DB_PATH)
    for r in hamta_senaste(20):
        print(r)