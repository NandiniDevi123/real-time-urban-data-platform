import re
from typing import List
from backend.app.schemas.agent_models import ToolCall

class ReasoningAgent:
    """
    Minimal agent:
    1) Detect intent from user query
    2) Build a tool-call plan (placeholder for now)
    """

    def detect_intent(self, query: str) -> str:
        q = query.lower()

        has_weather = any(w in q for w in ["weather", "temperature", "temp", "forecast", "rain", "snow", "humidity", "wind"])
        has_aqi = any(w in q for w in ["aqi", "air quality", "pollution", "pm2.5", "pm10", "o3", "no2", "smoke"])

        if has_weather and has_aqi:
            return "combined"
        if has_weather:
            return "weather"
        if has_aqi:
            return "aqi"
        return "general"

    def extract_location_hint(self, query: str) -> str:
        """
        Simple placeholder location extraction.
        For now: if user writes 'in <place>' or 'at <place>', capture it.
        This will improve later with a proper geocoding tool.
        """
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

        return []  # general chat: no tools

    def respond(self, query: str):
        intent = self.detect_intent(query)
        plan = self.build_plan(intent, query)

        # Placeholder response (later it will call tools and summarize results)
        if intent == "general":
            msg = "This request doesn’t look like weather or air quality. Ask for weather, AQI, or both (example: 'weather and AQI in Detroit')."
        else:
            msg = f"Intent detected: {intent}. Tool plan created (next step is executing tools)."

        return intent, plan, msg