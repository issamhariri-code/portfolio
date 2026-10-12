import pandas as pd

def create_dataframe(records):
    """
    Skapar en pandas DataFrame från en lista med dictionarys.
    Om input är felaktig kastas ett ValueError.
    """
    # Om records inte är en lista blir det fel
    if type(records) != list:
        raise ValueError("Input måste vara en lista")
    
    # Om listan är tom returnera tom dataframe med kolumner
    if len(records) == 0:
        return pd.DataFrame(columns=["time_start", "SEK_per_kWh"])
    
    # Omvandla JSON-listan till DataFrame för enkel hantering och tabellvisning
    df = pd.DataFrame(records)
    return df