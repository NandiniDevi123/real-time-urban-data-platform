import httpx
from typing import Dict, Any

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

def geocode_city(city: str) -> Dict[str, Any]:
    """
    Convert a city name into lat/lon using Open-Meteo geocoding (no auth).
    """
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    with httpx.Client(timeout=10) as client:
        r = client.get(GEOCODE_URL, params=params)
        r.raise_for_status()
        data = r.json()

    results = data.get("results") or []
    if not results:
        raise ValueError(f"Could not find location for '{city}'")

    top = results[0]
    return {
        "name": top.get("name"),
        "country": top.get("country"),
        "admin1": top.get("admin1"),
        "latitude": top.get("latitude"),
        "longitude": top.get("longitude"),
    }