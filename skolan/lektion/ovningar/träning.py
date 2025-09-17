klass = {
    "elever": ["Morgan", "Veronica", "Sofia", "Emil", "Hanna"],
    "klassrum": 'c401',
}

print("Elever = ", str(klass["elever"]))

# Lägg till nytt namn
elever: list = klass["elever"]
elever.append("Issam Hariri")

klassrum = klass["klassrum"]

# Lägg till rad i filen (append-läge 'a')
with open('baratext.txt', 'a', encoding='utf-8') as file_obj:
    file_obj.write('Issam Hariri, login, 20240908\n')

# Läs ut alla rader från filen och skriv ut
with open('baratext.txt', encoding='utf-8') as file_obj:
    for line in file_obj.readlines():
        print("rad:" + line.strip())
print("Klassrum =", klassrum)