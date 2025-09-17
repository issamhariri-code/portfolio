def to_do_app():
    uppgifter = [
        {"titel": "Läxor", "Kategori": "Studier", "klar": False},
        {"titel": "Handla", "Kategori": "Mathandel", "klar": False},
        {"titel": "Träning", "Kategori": "MMA", "klar": False}
    ]

    print("Menyval:\n1. Visa alla uppgifter\n2. Lägg till ny uppgift\n3. Markera som klar\n4. Avsluta")

    while True:
        val = int(input("Välj ett alternativ: "))
        if val == 1:
            for f in uppgifter:
                f["Kategori"]
                print (f["Kategori"])

to_do_app()