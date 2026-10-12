"""Offline checks of the relocated electricity-price application."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from importlib import import_module
from datetime import date, timedelta

module = import_module("ElprisApp.app")

def test_home_and_404():
    module.app.config.update(TESTING=True)
    client = module.app.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/missing").status_code == 404

def test_results_render(monkeypatch):
    monkeypatch.setattr(module, "get_elpriser", lambda *args: [
        {"time_start": "00:00", "SEK_per_kWh": 0.5}
    ])
    day = date.today() - timedelta(days=3)
    response = module.app.test_client().post("/result", data={
        "year": day.year, "month": day.month, "day": day.day, "area": "SE3"
    })
    assert response.status_code == 200
    assert "0.5" in response.get_data(as_text=True)

def test_invalid_data_type_rejected():
    import pytest
    from ElprisApp.utils.data_tools import create_dataframe
    with pytest.raises(ValueError):
        create_dataframe(None)
