#skapa en liten ordbok i en dictionary
# användaren kan skriva in ett ord på svenska och få det översatt till engelska
# Användaren kan även lägga till nya ord i ordboken

ordbok = {
    "hej": "hello",
    "hund": "dog",
    "katt": "cat",
    "bil": "car",
    "hus": "house"}

def översätt_ord(ordbok):
    while True:
        svenskt_ord = input("Skriv ett svenskt ord att översätta (eller 'avsluta' för att sluta): " \
        "eller 'lägg till' för att lägga till ett nytt ord: ")
        if svenskt_ord.lower() == "avsluta":
            break
        elif svenskt_ord.lower() == "lägg till":
            nytt_ord = input("Skriv det svenska ordet du vill lägga till: ")
            engelsk_översättning = input("Skriv den engelska översättningen: ")
            ordbok[nytt_ord] = engelsk_översättning
            print(f"Lagt till: {nytt_ord} -> {engelsk_översättning}")
        elif svenskt_ord in ordbok:
            print(f"{svenskt_ord} på engelska är {ordbok[svenskt_ord]}")
        else:
            print(f"Ordet '{svenskt_ord}' finns inte i ordboken.")
översätt_ord(ordbok)