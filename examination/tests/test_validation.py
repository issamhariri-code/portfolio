"""
filen ska stoppa felaktig indata och släppa igenom korrekt.
testområde:
datum saknas - fel
fel format - fel
datum före 2022 - 11 - 01 blir fel och datum i framtiden blir fel. Giltigt datum OK.

tickers:
inga tickers blir fel. fler än 10 Tickers blir fel. ogiltiga tecken blir fel.
blandade versaler är OK små/stor.
whitespace runt poster trimmas.

output:
valid True eller False . True om allting är godkänt. 
False om något var fel, exempelvis datum i framtiden.
errors - rätt felmeddelanden, om användaren lämnar en tom sträng på datum
så blir en error "Ange ett datum"
"""

"""
test_validation.py
Testar validation.py – alla felmeddelanden, edge cases, säkerhet
Kör med: pytest test_validation.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.validation import validate_input
from datetime import date, datetime, timedelta


#  Testa tomma eller saknade värden 
def test_no_date():
    result = validate_input("AAPL", None)
    assert not result["valid"]
    assert "Ange ett datum" in result["errors"]

def test_empty_date():
    result = validate_input("AAPL", "")
    assert not result["valid"]
    assert "Ange ett datum" in result["errors"]

def test_no_tickers():
    result = validate_input(None, "2025-10-31")
    assert not result["valid"]
    assert "Ange minst en ticker" in result["errors"]

def test_empty_tickers():
    result = validate_input("", "2025-10-31")
    assert not result["valid"]
    assert "Ange minst en ticker" in result["errors"]


#  Testa ogiltigt datumformat 
def test_invalid_date_format():
    result = validate_input("AAPL", "2025/10/31")
    assert not result["valid"]
    assert "Ogiltigt datumformat" in result["errors"]

    result = validate_input("AAPL", "2025-10")
    assert not result["valid"]
    assert "Ogiltigt datumformat" in result["errors"]

    result = validate_input("AAPL", "2025-10-31-00")
    assert not result["valid"]
    assert "Ogiltigt datumformat" in result["errors"]


#  Testa datum före minsta tillåtna (2022-11-01) 
def test_date_too_old():
    result = validate_input("AAPL", "2022-10-31")
    assert not result["valid"]
    assert "Datum får inte vara före 2022-11-01" in result["errors"]


#  Testa framtida datum
def test_future_date():
    future = (date.today() + timedelta(days=1)).isoformat()
    result = validate_input("AAPL", future)
    assert not result["valid"]
    assert "Datum får inte vara i framtiden" in result["errors"]


# Testa max 10 tickers
def test_too_many_tickers():
    tickers = ",".join([f"TICK{i}" for i in range(11)])  # 11 tickers
    result = validate_input(tickers, "2025-10-31")
    assert not result["valid"]
    assert "Max 10 tickers" in result["errors"]


#  Testa ogiltiga tecken 
def test_invalid_characters():
    result = validate_input("AAPL!,TSLA$", "2025-10-31")
    assert not result["valid"]
    assert "Ogiltiga tecken i AAPL!" in result["errors"] or "Ogiltiga tecken i TSLA$" in result["errors"]

    result = validate_input("AAPL@NVDA", "2025-10-31")
    assert not result["valid"]
    assert "Ogiltiga tecken i AAPL@NVDA" in result["errors"]


#  Testa giltiga fall 
def test_valid_single_ticker():
    result = validate_input("AAPL", "2025-10-31")
    assert result["valid"]
    assert result["clean"]["items"] == ["AAPL"]
    assert result["clean"]["date"] == date(2025, 10, 31)

def test_valid_multiple_tickers():
    result = validate_input("aapl, tsla, nvda", "2025-10-31")
    assert result["valid"]
    assert sorted(result["clean"]["items"]) == ["AAPL", "NVDA", "TSLA"]

def test_valid_with_spaces_and_duplicates():
    result = validate_input("  AAPL ,  aapl  , TSLA ,   ", "2025-10-31")
    assert result["valid"]
    assert result["clean"]["items"] == ["AAPL", "TSLA"]  # deduped


#  Testa edge cases: tomma strängar efter split 
def test_empty_items_after_split():
    result = validate_input(",,,   ,", "2025-10-31")
    assert not result["valid"]
    assert "Ange minst en ticker" in result["errors"]


#  Testa exakt 10 tickers 
def test_exactly_10_tickers():
    tickers = ",".join([f"TICK{i}" for i in range(10)])
    result = validate_input(tickers, "2025-10-31")
    assert result["valid"]
    assert len(result["clean"]["items"]) == 10


# Testa tillåtna specialtecken: 
def test_allowed_characters():
    result = validate_input("BRK.A, BRK-B, TSLA-1", "2025-10-31")
    assert result["valid"]
    assert result["clean"]["items"] == ["BRK.A", "BRK-B", "TSLA-1"]


#  Testa att datum konverteras rätt (ISO-format) 
def test_date_conversion():
    result = validate_input("AAPL", "2023-01-15")
    assert result["valid"]
    assert result["clean"]["date"] == date(2023, 1, 15)


# Testa att min_date funkar
def test_min_date_edge():
    result = validate_input("AAPL", "2022-11-01")
    assert result["valid"]  # exakt minsta datum = OK

    result = validate_input("AAPL", "2022-10-31")
    assert not result["valid"]  # en dag före = FEL