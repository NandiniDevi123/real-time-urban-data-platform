from datetime import datetime, timezone
from typing import Dict, Any
import httpx

from backend.app.tools.geocode_tool import geocode_city

AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

def get_aqi(location: str) -> Dict[str, Any]:
    geo = geocode_city(location)

    params = {
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        # ✅ Correct Open-Meteo variable names:
        "current": "european_aqi,pm2_5,pm10,ozone,nitrogen_dioxide",
        "timezone": "UTC",
    }

    with httpx.Client(timeout=15) as client:
        r = client.get(AQI_URL, params=params)
        r.raise_for_status()
        data = r.json()

    current = data.get("current") or {}
    return {
        "location": f'{geo["name"]}, {geo.get("admin1","")}, {geo.get("country","")}'.strip(", "),
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "aqi": current.get("european_aqi"),
        "pm25": current.get("pm2_5"),
        "pm10": current.get("pm10"),
        "ozone": current.get("ozone"),
        "nitrogen_dioxide": current.get("nitrogen_dioxide"),
        "timestamp": current.get("time") or datetime.now(timezone.utc).isoformat(),
        "source": "open-meteo-air-quality",
    }