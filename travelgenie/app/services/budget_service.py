def parse_budget(budget_str):

    if not budget_str:
        return 0

    budget_str = str(budget_str).upper().replace(",", "").replace("₹", "").strip()

    try:

        if "K" in budget_str:
            value = float(budget_str.replace("K", ""))
            return int(value * 1000)

        if "L" in budget_str:
            value = float(budget_str.replace("L", ""))
            return int(value * 100000)

        return int(float(budget_str))

    except Exception:
        # fallback if user types something weird
        return 0


def split_budget(budget):

    total = parse_budget(budget)

    return {
        "stay": int(total * 0.40),
        "food": int(total * 0.25),
        "transport": int(total * 0.20),
        "activities": int(total * 0.15)
    }