CITY_CURRENCY = {

    "mumbai": ("INR", "₹"),
    "delhi": ("INR", "₹"),
    "bangalore": ("INR", "₹"),

    "paris": ("EUR", "€"),
    "rome": ("EUR", "€"),
    "berlin": ("EUR", "€"),

    "new york": ("USD", "$"),
    "los angeles": ("USD", "$"),

    "tokyo": ("JPY", "¥"),
}


def get_currency_for_city(city):

    city = city.lower()

    return CITY_CURRENCY.get(city, ("USD", "$"))