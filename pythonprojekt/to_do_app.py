def to_do_app():
    uppgifter = [
        {"Titel": "Läxor:", "Kategori": "Studier", "klar": False},
        {"Titel": "Handla:", "Kategori": "Mathandel", "klar": False},
        {"Titel": "Träning:", "Kategori": "MMA", "klar": False}
    ]


    while True:
        print("Menyval:\n1. Visa alla uppgifter\n2. Lägg till ny uppgift\n3. Markera som klar\n4. Avsluta")
        val = int(input("Välj ett alternativ: "))
        if val == 1:
            for f in uppgifter:
                if f["klar"]:
                    status = "[x]"
                else:
                    status = "[ ]"
                print (status, f["Titel"], f["Kategori"])

        elif val == 3:
            if uppgifter == [ ]:
                print("Inga uppgifter att markera")
                continue
            else:
                for f in uppgifter:
                    print (f["Titel"], f["Kategori"])
                try:
                    val_nummer = int(input("Vilken uppgift vill du markera som klar? Ange numret:"))
                    if val_nummer < 1 or val_nummer > len(uppgifter):
                        print("Ange korrekt alterntiv")
                        continue
                except ValueError:
                    print("Ange en siffra")
                    continue

                index = val_nummer -1
                if uppgifter[index]["klar"]:
                    print("Redan klar")

                else:
                    uppgifter[index]["klar"] = True
                    print("Markerad som klar!")

        elif val == 4:
            print("Vi ses nästa gång")
            break

                            

to_do_app()