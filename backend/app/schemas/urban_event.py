from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UrbanEvent(BaseModel):
    source: str                 # e.g., "traffic", "weather", "aqi"
    location: str               # e.g., "Detroit Downtown"
    value: float                # numeric metric
    unit: str                   # e.g., "mph", "C", "AQI"
    timestamp: Optional[datetime] = None