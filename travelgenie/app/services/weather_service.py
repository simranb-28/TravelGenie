import httpx
from app.core.config import settings
from app.services.cache_service import get_cache, set_cache


async def get_weather(destination: str):

    cache_key = f"weather:{destination.lower()}"

    cached = get_cache(cache_key)
    if cached:
        print("Using cached weather.")
        return cached

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": destination,
        "appid": settings.WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, params=params)
            print(f"Weather API Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Weather API Error Response: {response.text}")
                return "Unknown"
                
            data = response.json()
            
            if "weather" not in data or len(data["weather"]) == 0:
                print(f"Invalid weather response: {data}")
                return "Unknown"

            weather_main = data["weather"][0]["main"]
            
            set_cache(cache_key, weather_main, expiry=1800)
            print(f"Weather fetched for {destination}: {weather_main}")

            return weather_main

    except Exception as e:
        print(f"Weather API error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return "Unknown"