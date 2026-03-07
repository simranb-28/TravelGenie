from google import genai
from app.core.config import settings
from app.services.cache_service import get_cache, set_cache
import json

# Initialize client lazily to handle missing API key
client = None

def get_client():
    global client
    if client is None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set. Please set the environment variable.")
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return client


# =========================================
# SAFE MODEL SELECTION
# =========================================
_model_name = None

def get_model_name():
    global _model_name
    if _model_name is None:
        models = get_client().models.list()
        for model in models:
            name = model.name
            if (
                name.startswith("models/gemini")
                and "embedding" not in name
                and "vision" not in name
            ):
                _model_name = name
                return name
        raise Exception("No compatible Gemini model found.")
    return _model_name


# =========================================
# INTENT EXTRACTION
# =========================================
async def extract_trip_intent(user_input: str):

    try:

        response = get_client().models.generate_content(
            model=get_model_name(),
            contents=user_input
        )

        if not response.text:
            return {}

        text = response.text.strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return {}

        return json.loads(text[start:end+1])

    except Exception as e:

        print("Intent extraction error:", e)
        return {}


# =========================================
# ACTIVITY GENERATION
# =========================================
async def generate_destination_activities(destination, preferences):

    # normalize preferences
    if not preferences:
        preferences = []

    if isinstance(preferences, str):
        preferences = [preferences]

    pref_text = ",".join(preferences).lower()

    cache_key = f"activities:{destination.lower()}:{pref_text}"

    cached = get_cache(cache_key)

    if cached:
        print("Using cached activities")
        return cached

    prompt = f"""
You are a travel planning AI.

Generate 15 realistic travel activities in {destination}.

User preferences: {pref_text}

Rules:
- If preference includes "food", prioritize food markets, street food tours, cafes, restaurants.
- If preference includes "culture" or "history", prioritize museums, monuments, heritage areas.
- If preference includes "nature", prioritize parks, viewpoints, beaches.

Return ONLY valid JSON.

Format:

[
  {{
    "name": "Street Food Tour in Colaba",
    "estimated_cost": 25,
    "base_score": 9,
    "tags": ["food"],
    "type": "food"
  }}
]
"""

    try:

        response = get_client().models.generate_content(
            model=get_model_name(),
            contents=prompt
        )

        if not response.text:
            print("Empty LLM response")
            return []

        text = response.text.strip()

        # remove markdown if Gemini adds ```json
        text = text.replace("```json", "").replace("```", "")

        start = text.find("[")
        end = text.rfind("]")

        if start == -1 or end == -1:
            print("JSON not found in response:", text)
            return []

        raw = json.loads(text[start:end+1])

        cleaned = []

        for act in raw:

            try:

                cleaned.append({
                    "name": act["name"],
                    "cost": int(act["estimated_cost"]),
                    "score": int(act["base_score"]),
                    "tags": act.get("tags", []),
                    "type": act.get("type", "general")
                })

            except Exception:
                continue

        if cleaned:

            set_cache(cache_key, cleaned, expiry=86400)
            print("Cached activities")

        return cleaned

    except Exception as e:

        print("Activity generation error:", e)
        return []