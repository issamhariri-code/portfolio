"""BEGIN
    OUTPUT "Välj konvertering: 1 för Celsius till Fahrenheit, 2 för Fahrenheit till Celsius"
    READ val FROM användarens_inmatning

    OM val = 1 DÅ
        READ celsius FROM användarens_inmatning
        fahrenheit = (celsius * 9/5) + 32
        OUTPUT celsius, "Celsius är", fahrenheit, "Fahrenheit"
    ANNARS om val = 2 DÅ
        READ fahrenheit FROM användarens_inmatning
        celsius = (fahrenheit - 32) * 5/9
        OUTPUT fahrenheit, "Fahrenheit är", celsius, "Celsius"
    ANNORS
        OUTPUT "Ogiltigt val."
END"""
print("Program för att konvertera Celsius till Fahrenheit")
fahrenheit = 0
celsius = 0

try:
    val = anv_inm = int(input("Välj konvertering 1 för Celsius till Fahrenheit, 2 för Fahrenheit till Celsius: ")) 
    
    if val == 1:
        celsius = int(input("Ange temperatur: "))
        fahrenheit = (celsius * 9/5) + 32
        print(f"{celsius}° är {fahrenheit}°F")
    
    elif val == 2:
        fahrenheit = int(input("Ange temperatur: "))
        celsius = (fahrenheit - 32) * 5/9
        print(f"{fahrenheit}°F är {celsius}°")
        
    else:
        print("Ogiltig val")

except ValueError:
    print("Fel: Du måste ange ett numeriskt värde.")




