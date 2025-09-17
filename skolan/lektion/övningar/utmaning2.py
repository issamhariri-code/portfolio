"""BEGIN
    READ nummer1 FROM användarens_inmatning
    READ nummer2 FROM användarens_inmatning
    READ nummer3 FROM användarens_inmatning

    OM nummer1 > nummer2 OCH nummer1 > nummer3 DÅ
        OUTPUT "Det största talet är:", nummer1
    ANNARS om nummer2 > nummer1 OCH nummer2 > nummer3 DÅ
        OUTPUT "Det största talet är:", nummer2
    ANNARS
        OUTPUT "Det största talet är:", nummer3
END"""
användare_inmatning = int(input("Ange ett tal"))
användare2_inmatning = int(input("Ange ett tal"))
användare3_inmatning = int(input("Ange ett tal"))

if användare_inmatning > användare2_inmatning and användare_inmatning > användare3_inmatning:
    print("Största talet är: första användaren ", användare_inmatning)

elif användare2_inmatning > användare_inmatning and användare2_inmatning > användare3_inmatning:
    print("Det största talet är: andra användaren", användare2_inmatning)

else:
    print("Största talet är: tredje användaren", användare3_inmatning)