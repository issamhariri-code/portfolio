def to_do_app():
    uppgifter = [
        {"Titel": "Läxor:", "Kategori": "Studier", "klar": False},
        {"Titel": "Handla:", "Kategori": "Mathandel", "klar": False},
        {"Titel": "Träning:", "Kategori": "MMA", "klar": False}
    ]

    print("Menyval:\n1. Visa alla uppgifter\n2. Lägg till ny uppgift\n3. Markera som klar\n4. Avsluta")

    while True:
        val = int(input("Välj ett alternativ: "))
        if val == 1:
            for f in uppgifter:
                f["Kategori"]
                print (f["Kategori"])

        elif val == 3:
            if uppgifter == []:
                print("Inga uppgifter att markera")
            else:
                for f in uppgifter:
                    print (f["Titel"], f["Kategori"])
            try:
                val_nummer = int(input("Vilken uppgift vill du markera som klar? Ange numret:"))
                if val_nummer < 1 or val_nummer > len(uppgifter):
                    print("Ange korrekt alterntiv")
            except ValueError:
                print("Ange en siffra")

            index = val_nummer -1
            if uppgifter[index]["klar"]:
                print("Redan klar")

            else:
                uppgifter[index]["klar"] = True
                print("Markerad som klar!")

                            

to_do_app()