"""
tester för utils.api_handler.get_elpriser

tester:
testa att funktionen går att anropa utan fel
resultat ska vara av rätt typ
testa att datan om den finns, har rätt struktur.

"""

from ElprisApp.utils.api_handler import get_elpriser

def test_get_elpriser_returns_data():
    """
    testar att funktionen går att anropa och returnerar något
    """
    data = get_elpriser(2025, 10, 26, "SE3")
    assert data is not None


def test_get_elpriser_returns_list():
    """
    funktionen ska returnera en lista (även om tom).
    """
    data = get_elpriser(2025, 10, 26, "SE3")

    assert type(data) == list 
    #Funktionen ska returnera en lista

def test_get_elpriser_item_structure():
    data = get_elpriser(2025, 10, 26, "SE3")

    # Om listan inte är tom
    if len(data) > 0:
        first = data[0]

        # Kontrollera att första elementet är en dict
        assert type(first) == dict

        # Kontrollera att nycklarna finns
        assert "time_start" in first
        assert "SEK_per_kWh" in first







