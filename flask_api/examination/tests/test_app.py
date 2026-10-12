"""Offline checks for the application after the repository move."""
import sys
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from application import create_app
from services import api_client

@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()

@pytest.mark.parametrize("path,status", [("/", 200), ("/about", 200), ("/missing", 404)])
def test_pages_render(client, path, status):
    assert client.get(path).status_code == status

def test_empty_form_is_rejected_without_api_call(client, monkeypatch):
    monkeypatch.setattr(api_client, "fetch_prices", lambda *args: pytest.fail("Unexpected API call"))
    response = client.post("/", data={"tickers": "", "date": "2025-01-03"})
    assert response.status_code == 200
    assert "Ange minst en ticker" in response.get_data(as_text=True)

def test_results_render_with_api_response(client, monkeypatch):
    monkeypatch.setattr(api_client, "fetch_prices", lambda *args: {
        "data": [{"ticker": "AAPL", "name": "Apple Inc.", "date": "2025-01-03",
                  "open": 100.0, "high": 110.0, "low": 95.0, "close": 105.0, "pct_change": 5.0}],
        "warnings": []
    })
    response = client.post("/", data={"tickers": "AAPL", "date": "2025-01-03", "perspective": "daily"})
    assert response.status_code == 200
    assert "AAPL" in response.get_data(as_text=True)

def test_missing_key_makes_no_request(monkeypatch):
    monkeypatch.setattr(api_client, "API_KEY", "")
    monkeypatch.setattr(api_client.requests, "get", lambda *args, **kwargs: pytest.fail("Unexpected request"))
    assert api_client.fetch_from_marketstack("AAPL", date(2025, 1, 3)) is None

def test_configured_key_is_used(monkeypatch):
    monkeypatch.setattr(api_client, "API_KEY", "test-only-placeholder")
    calls = []
    class Response:
        status_code = 200
        def json(self):
            return {"data": [{"open": 10, "high": 12, "low": 9, "close": 11}]}
    def request(url, **kwargs):
        calls.append((url, kwargs))
        return Response()
    monkeypatch.setattr(api_client.requests, "get", request)
    quote = api_client.fetch_from_marketstack("AAPL", date(2025, 1, 3))
    assert quote["close"] == 11.0
    assert calls[0][1]["params"]["access_key"] == "test-only-placeholder"
