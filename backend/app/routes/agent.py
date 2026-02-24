from fastapi import APIRouter, HTTPException

from backend.app.agent.reasoning_agent import ReasoningAgent
from backend.app.schemas.agent_models import AgentRequest, AgentResponse
from backend.app.tools.weather_tool import get_weather
from backend.app.tools.aqi_tool import get_aqi

router = APIRouter(prefix="/agent", tags=["Agent"])
agent = ReasoningAgent()


def build_summary(tool_results: list) -> str:
    weather = next((r for r in tool_results if r.get("source") == "open-meteo"), None)
    aqi = next((r for r in tool_results if r.get("source") == "open-meteo-air-quality"), None)

    parts = []

    if weather:
        loc = weather.get("location", "Location")
        temp = weather.get("temperature_c")
        hum = weather.get("humidity_pct")
        wind = weather.get("wind_kph")
        parts.append(f"{loc}: {temp}°C, humidity {hum}%, wind {wind} km/h.")

    if aqi:
        loc = aqi.get("location", "Location")
        aqi_val = aqi.get("aqi")
        pm25 = aqi.get("pm25")
        pm10 = aqi.get("pm10")
        ozone = aqi.get("ozone")
        no2 = aqi.get("nitrogen_dioxide")
        parts.append(
            f"AQI for {loc}: {aqi_val}. PM2.5 {pm25}, PM10 {pm10}, Ozone {ozone}, NO2 {no2}."
        )

    if not parts:
        return "No results available yet."

    return " ".join(parts)


@router.post("/query", response_model=AgentResponse)
def agent_query(payload: AgentRequest):
    intent, plan, _ = agent.respond(payload.query)

    tool_results = []
    try:
        for call in plan:
            loc = call.arguments.get("location", "unknown")

            if call.tool_name == "get_weather":
                tool_results.append(get_weather(loc))

            elif call.tool_name == "get_aqi":
                tool_results.append(get_aqi(loc))

    except ValueError as e:
        # geocoding could not find the city
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # API/network issues (timeouts, 400s, etc.)
        raise HTTPException(status_code=502, detail=f"Tool execution failed: {str(e)}")

    message = build_summary(tool_results)

    return AgentResponse(
        intent=intent,
        plan=plan,
        message=message,
        tool_results=tool_results,
        notes="Real tool execution enabled (Card 3)."
    )