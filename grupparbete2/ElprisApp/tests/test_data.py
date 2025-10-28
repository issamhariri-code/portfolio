from utils.data_tools import create_dataframe

def test_create_dataframe():
    sample = [{"time_start":"00:00","SEK_per_kWh":0.5}]
    df = create_dataframe(sample)
    assert "time_start" in df.columns and "SEK_per_kWh" in df.columns
