from utils.api_handler import get_elpriser

def test_get_elpriser_returns_data():
    data = get_elpriser(2025, 10, 26, "SE3")
    assert data is not None
