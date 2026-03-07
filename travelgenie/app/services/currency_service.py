import requests


def convert_currency(amount_usd: float, currency: str):

    try:

        url = f"https://api.exchangerate.host/convert?from=USD&to={currency}&amount={amount_usd}"

        response = requests.get(url)

        data = response.json()

        return round(data["result"], 2)

    except Exception:
        return amount_usd