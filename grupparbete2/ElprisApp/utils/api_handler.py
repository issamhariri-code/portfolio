import requests

def get_elpriser(year: int, month: int, day: int, area: str):
    month_str = f"{month:02d}"
    day_str = f"{day:02d}"
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month_str}-{day_str}_{area}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Fel vid API-anrop:", e)
        return None

#Anropa API:et med valt datum och område
#Returnera data som lista av dict
