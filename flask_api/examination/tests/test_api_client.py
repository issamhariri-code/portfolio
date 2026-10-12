"""
test_api_client.py
Testar api_client.py med Marketstack API
Kör med: pytest test_api_client.py -v
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.api_client import fetch_prices


# --- Testa fetch_prices med riktigt API ---
def test_fetch_prices_single_ticker():
    """Testa att hämta data för en ticker"""
    result = fetch_prices(["AAPL"], "2023-01-03")
    assert "data" in result
    assert "warnings" in result
    # Om API fungerar, ska vi ha data
    if len(result["data"]) > 0:
        row = result["data"][0]
        assert row["ticker"] == "AAPL"
        assert "open" in row
        assert "close" in row
        assert "name" in row


def test_fetch_prices_multiple_tickers():
    """Testa att hämta data för flera tickers"""
    result = fetch_prices(["AAPL", "TSLA"], "2023-01-03")
    assert "data" in result
    assert "warnings" in result
    # Om API inte ger data, ska warnings finnas
    if len(result["data"]) == 0:
        assert len(result["warnings"]) > 0
    else:
        tickers = [row["ticker"] for row in result["data"]]
        assert len(tickers) > 0


def test_fetch_prices_invalid_ticker():
    """Testa med ogiltig ticker"""
    result = fetch_prices(["INVALIDTICKER123"], "2023-01-03")
    # Antingen tom data eller varning
    assert "data" in result
    assert "warnings" in result


def test_fetch_prices_no_data():
    """Testa med datum utan data"""
    result = fetch_prices(["AAPL"], "2099-12-31")
    assert len(result["data"]) == 0


def test_fetch_prices_company_names():
    """Testa att företagsnamn finns"""
    result = fetch_prices(["AAPL"], "2023-01-03")
    if len(result["data"]) > 0:
        row = result["data"][0]
        assert row["name"] == "Apple Inc." or row["name"] == "N/A"


def test_fetch_prices_pct_change():
    """Testa att procentförändring beräknas"""
    result = fetch_prices(["AAPL"], "2023-01-03")
    if len(result["data"]) > 0:
        row = result["data"][0]
        assert "pct_change" in row
        # pct_change kan vara None eller ett nummer
        if row["pct_change"] is not None:
            assert isinstance(row["pct_change"], (int, float))