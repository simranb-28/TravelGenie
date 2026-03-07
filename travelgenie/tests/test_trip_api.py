from fastapi.testclient import TestClient
from app.main import app


async def mock_generate_trip(request):
    return {
        "destination": request.destination,
        "duration": request.duration,
        "weather": "Clear",
        "budget_allocation": {
            "stay": 500,
            "food": 200,
            "activities": 300,
            "transport": 100
        },
        "selected_activities": [
            ["Test Activity", 100, 8]
        ],
        "itinerary": [
            "Day 1: Arrival",
            "Day 2: Test Activity",
            "Day 3: Departure"
        ],
        "why_this_plan": "Mocked response"
    }


def test_generate_trip(monkeypatch):

    monkeypatch.setattr(
        "app.api.routes.generate_trip",
        mock_generate_trip
    )

    client = TestClient(app)

    payload = {
        "destination": "Rome",
        "duration": 3,
        "budget": 1000,
        "preferences": ["food"]
    }

    response = client.post("/generate-trip", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["destination"] == "Rome"
    assert "itinerary" in data