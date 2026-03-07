def knapsack_optimize(activities, budget):
    """
    activities: list of dicts
    each activity -> {name, cost, score}

    Returns optimal list of activities within budget
    """

    if not activities or budget <= 0:
        return []

    # Normalize budget (reduce DP size)
    scale = 10
    norm_budget = budget // scale

    norm_activities = []

    for act in activities:
        cost = act["cost"] // scale
        if cost <= norm_budget and cost > 0:
            norm_activities.append({
                "original": act,
                "cost": cost,
                "score": act["score"]
            })

    if not norm_activities:
        return []

    n = len(norm_activities)

    dp = [[0]*(norm_budget+1) for _ in range(n+1)]

    for i in range(1, n+1):

        cost = norm_activities[i-1]["cost"]
        score = norm_activities[i-1]["score"]

        for b in range(norm_budget+1):

            if cost <= b:
                dp[i][b] = max(
                    score + dp[i-1][b-cost],
                    dp[i-1][b]
                )
            else:
                dp[i][b] = dp[i-1][b]

    # Backtrack
    selected = []
    b = norm_budget

    for i in range(n, 0, -1):

        if dp[i][b] != dp[i-1][b]:

            selected.append(norm_activities[i-1]["original"])
            b -= norm_activities[i-1]["cost"]

    return selected[::-1]