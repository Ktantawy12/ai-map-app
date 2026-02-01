
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = """You are a geospatial assistant.
Extract structured parameters from the user's query for the following tools:

- place: string (where)
- layer_type: one of: restaurant, cafe, hospital, pharmacy, school, bank, fuel, supermarket, park
- radius_km: number (km)

Return ONLY valid JSON with keys: place, layer_type, radius_km.
No markdown. No extra keys.
"""

def llm_parse_query(user_query: str) -> dict:
    if not os.getenv("OPENAI_API_KEY"):
        return {"ok": False, "error": "Missing OPENAI_API_KEY"}

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_query},
            ],
        )

        txt = resp.choices[0].message.content.strip()
        data = json.loads(txt)

        # minimal validation + defaults
        place = str(data.get("place", "")).strip()
        layer_type = str(data.get("layer_type", "restaurant")).strip().lower()
        radius_km = float(data.get("radius_km", 3))

        allowed = {"restaurant","cafe","hospital","pharmacy","school","bank","fuel","supermarket","park"}
        if layer_type not in allowed:
            layer_type = "restaurant"

        radius_km = max(0.2, min(radius_km, 50.0))
        if not place:
            return {"ok": False, "error": "LLM could not extract a place."}

        return {"ok": True, "place": place, "layer_type": layer_type, "radius_km": radius_km}

    except Exception as e:
        return {"ok": False, "error": f"LLM parse failed: {e}"}
