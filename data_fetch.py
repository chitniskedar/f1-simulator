import requests
import pandas as pd

BASE_URL = "https://api.jolpi.ca/ergast/f1"
headers = {"User-Agent": "Mozilla/5.0"}


def fetch_qualifying(year):
    url = f"{BASE_URL}/{year}/qualifying.json?limit=2000"
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    races = data["MRData"]["RaceTable"]["Races"]

    records = []

    for race in races:
        circuit = race["Circuit"]["circuitName"]

        for result in race["QualifyingResults"]:
            driver = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
            driver = driver.replace("ü", "u")

            records.append({
                "year": year,
                "circuit": circuit,
                "driver": driver,
                "position": int(result["position"])
            })

    return pd.DataFrame(records)


def fetch_race(year):
    url = f"{BASE_URL}/{year}/results.json?limit=2000"
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    races = data["MRData"]["RaceTable"]["Races"]

    records = []

    for race in races:
        for result in race["Results"]:
            driver = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
            driver = driver.replace("ü", "u")

            records.append({
                "year": year,
                "driver": driver,
                "position": int(result["position"])
            })

    return pd.DataFrame(records)
