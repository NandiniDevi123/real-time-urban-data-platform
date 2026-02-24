from datetime import datetime, timezone
from typing import Dict, Any
import httpx

from backend.app.tools.geocode_tool import geocode_city

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(location: str) -> Dict[str, Any]:
    """
    Real weather tool using Open-Meteo (no auth).
    Uses current weather via latitude/longitude.
    """
    geo = geocode_city(location)
    params = {
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
        "timezone": "UTC",
    }

    with httpx.Client(timeout=10) as client:
        r = client.get(WEATHER_URL, params=params)
        r.raise_for_status()
        data = r.json()

    current = data.get("current") or {}
    return {
        "location": f'{geo["name"]}, {geo.get("admin1","")}, {geo.get("country","")}'.strip(", "),
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "temperature_c": current.get("temperature_2m"),
        "humidity_pct": current.get("relative_humidity_2m"),
        "wind_kph": current.get("wind_speed_10m"),
        "timestamp": current.get("time") or datetime.now(timezone.utc).isoformat(),
        "source": "open-meteo",
    }