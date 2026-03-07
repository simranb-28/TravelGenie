from app.services.cache_service import get_cache, set_cache


def recommend_stays(destination: str, stay_budget: int, duration: int):

    per_night = stay_budget // max(duration - 1, 1)

    if per_night < 1500:

        stays = [
            "Local Guesthouses",
            "Budget Homestays",
            "Zostel / Backpacker Hostels"
        ]

    elif per_night < 4000:

        stays = [
            "3 Star Hotels",
            "Boutique Homestays",
            "Mid-range Resorts"
        ]

    else:

        stays = [
            "Luxury Resorts",
            "Premium Hotels",
            "Heritage Stays"
        ]

    return stays