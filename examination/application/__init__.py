"""Filen som startar motorn, denna fil körs innan app.py,
Startpunkten när flask laddar projektet,
__init__.py skapar själva objektet (flask(__name__)) samt returnerar det,
I filen skapar jag en funktion som heter create_app()
Flask känner igen funktionen och startar den.
Genom att ha en separat app.py fil och init.py fil så skapas en plats för
logik samt en plats för initiering."""