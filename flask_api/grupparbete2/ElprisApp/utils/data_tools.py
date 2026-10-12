import pandas as pd

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df

def create_dataframe(records):
    # Om records inte är en lista blir de felfel
    if type(records) != list: #om ej lista blir felmeddelande följande
        raise TypeError("Input måste vara en lista") #felmeddelande

    # om listan är tom returnera tom dataframe med kolumner
    if len(records) == 0:
        return pd.DataFrame(columns=["time_start", "SEK_per_kWh"])

    # else, skapa dataframe
    df = pd.DataFrame(records)

    # säkerställer att kolumnerna finns.
    if "time_start" not in df.columns:
        df["time_start"] = ""

    if "SEK_per_kWh" not in df.columns:
        df["SEK_per_kWh"] = 0.0

    return df    

#Omvandla JSON-listan till DataFrame för enkel hantering och tabellvisning