from app.services.optimization_service import knapsack_optimize


def test_knapsack_basic():

    activities = [
        ("Colosseum Tour", 100, 8),
        ("Vatican Museum", 150, 9),
        ("Food Tour", 120, 10),
    ]

    budget = 250

    result = knapsack_optimize(budget, activities)

    total_cost = sum(a[1] for a in result)

    assert total_cost <= budget
    assert len(result) > 0


def test_knapsack_zero_budget():

    activities = [
        ("Tour A", 100, 5),
        ("Tour B", 200, 6)
    ]

    result = knapsack_optimize(0, activities)

    assert result == []