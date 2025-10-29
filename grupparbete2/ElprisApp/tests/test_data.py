"""
tester för utils.data_tools.create_dataframe

testa att funktionen returnerar dataframe och testar att
kolumnerna finns
testa att felaktig input hanteras

"""


import pytest
import pandas as pd
from utils.data_tools import create_dataframe

def test_create_dataframe():
    sample = [{"time_start":"00:00","SEK_per_kWh":0.5}]
    df = create_dataframe(sample)
    assert "time_start" in df.columns and "SEK_per_kWh" in df.columns



def test_create_dataframe_handles_empty_list():
    # tom lista skickas in
    df = create_dataframe([])
    # df innehåller det som funktionen returnerar
    # i detta fall en pandas dataframe 

    # det ska fortfarande bli en dataframe
    assert type(df) == pd.DataFrame
    # funktionen kan hantera tom input
    # tom lista blir 0 rader 
    assert len(df) == 0

    # Kolumnerna måste finnas i tabellen 
    assert "time_start" in df.columns
    assert "SEK_per_kWh" in df.columns


def test_create_dataframe_invalid_input():
    """
    Enkel variant av feltest: vi anropar funktionen med None
    och kontrollerar att funktionen kastar ett fel.
    """

    try:
        create_dataframe(None)
        assert False #om funktionen inte hittar fel, fortsätter koden
        #assert False på rad 47 gör att testet misslyckas med felmeddelande.
    except:
        # Om vi hamnar här fungerar testet
        # då har funktionen hanterat felaktig input korrekt
        assert True

        """testet verifierarar att funktionen create_dataframe
          kastar ett undantag när den får None som input  """