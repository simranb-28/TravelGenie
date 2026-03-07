from app.services.llm_service import generate_destination_activities
from app.services.optimization_service import knapsack_optimize
from app.services.budget_service import split_budget
from app.services.weather_service import get_weather


# ===============================
# BUILD ITINERARY
# ===============================

def build_itinerary(activities, duration, alternative_activities=None):

    itinerary = []

    duration = int(duration)

    if duration <= 1:
        return ["Day 1: Arrival and explore nearby areas"]

    # Day 1 arrival
    itinerary.append("Day 1: Arrival and light exploration")

    activity_names = [a["name"] for a in activities]
    
    # Get alternative activities that are not in the main itinerary
    alternative_names = []
    if alternative_activities:
        selected_ids = {a.get("id") or a["name"] for a in activities}
        alternative_names = [
            a["name"] for a in alternative_activities 
            if (a.get("id") or a["name"]) not in selected_ids
        ]

    idx = 0
    alt_idx = 0

    # Middle days
    for day in range(2, duration):

        todays = activity_names[idx:idx + 3]
        idx += 3

        if todays:
            plan = ", ".join(todays)
        else:
            # If no activities from budget plan, use alternatives
            if alt_idx < len(alternative_names):
                alt_activities = alternative_names[alt_idx:alt_idx + 2]
                if alt_activities:
                    plan = ", ".join(alt_activities)
                    alt_idx += 2
                else:
                    plan = "Free exploration"
            else:
                plan = "Free exploration"

        itinerary.append(f"Day {day}: {plan}")

    # Last day
    itinerary.append(f"Day {duration}: Departure")

    return itinerary


# ===============================
# MAIN TRIP GENERATOR
# ===============================

async def generate_trip(request):

    destination = request.destination
    duration = request.duration
    budget = request.budget
    preferences = request.preferences

    # 1️⃣ Budget allocation
    budget_split = split_budget(budget)

    # 2️⃣ Generate candidate activities
    candidate_activities = await generate_destination_activities(
        destination,
        preferences
    )

    if not candidate_activities:
        candidate_activities = []

    # 3️⃣ Optimize activities within activity budget
    selected_activities = knapsack_optimize(
        candidate_activities,
        budget_split["activities"]
    )

    # 4️⃣ Build itinerary with alternative activities for free days
    itinerary = build_itinerary(selected_activities, duration, candidate_activities)

    # 5️⃣ Get weather
    weather = await get_weather(destination)
    print(f"Weather result: {weather}")

    # 6️⃣ Return response
    return {
        "destination": destination,
        "duration": duration,
        "budget": budget,
        "budget_allocation": budget_split,
        "recommended_experiences": selected_activities,
        "weather": weather,
        "itinerary": itinerary
    }