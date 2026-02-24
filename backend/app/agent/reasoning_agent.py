import re
from typing import List

from backend.app.schemas.agent_models import ToolCall


class ReasoningAgent:

    def detect_intent(self, query: str) -> str:
        q = query.lower()

        has_weather = any(
            w in q for w in ["weather", "temperature", "temp", "forecast", "rain", "snow", "humidity", "wind"]
        )
        has_aqi = any(
            w in q for w in ["aqi", "air quality", "pollution", "pm2.5", "pm10", "o3", "no2", "smoke"]
        )

        if has_weather and has_aqi:
            return "combined"
        if has_weather:
            return "weather"
        if has_aqi:
            return "aqi"
        return "general"

    def extract_location_hint(self, query: str) -> str:
        m = re.search(r"\b(in|at)\s+([a-zA-Z\s]+)$", query.strip(), re.IGNORECASE)
        if m:
            return m.group(2).strip()
        return "unknown"

    def build_plan(self, intent: str, query: str) -> List[ToolCall]:
        location = self.extract_location_hint(query)

        if intent == "weather":
            return [ToolCall(tool_name="get_weather", arguments={"location": location})]

        if intent == "aqi":
            return [ToolCall(tool_name="get_aqi", arguments={"location": location})]

        if intent == "combined":
            return [
                ToolCall(tool_name="get_weather", arguments={"location": location}),
                ToolCall(tool_name="get_aqi", arguments={"location": location}),
            ]

        return []

    def respond(self, query: str):
        intent = self.detect_intent(query)
        plan = self.build_plan(intent, query)
        location = self.extract_location_hint(query)

        if intent == "general":
            message = "Please ask for weather, AQI, or both. Example: 'weather and AQI in Detroit'."

        elif location == "unknown":
            message = "Please provide a city name so I can retrieve weather or AQI data."

        elif intent == "weather":
            message = f"I will retrieve weather data for {location}. Next step: call get_weather tool."

        elif intent == "aqi":
            message = f"I will retrieve air quality (AQI) data for {location}. Next step: call get_aqi tool."

        else:
            message = (
                f"I will retrieve both weather and AQI data for {location}. "
                "Next step: call get_weather and get_aqi tools."
            )

        return intent, plan, message