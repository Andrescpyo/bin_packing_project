import random

from src.heuristics import first_fit


def randomized_ffd(items, capacity):

    items_copy = sorted(
        items,
        reverse=True
    )

    n = len(items_copy)

    swaps = max(1, n // 20)

    for _ in range(swaps):

        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

        items_copy[i], items_copy[j] = (
            items_copy[j],
            items_copy[i]
        )

    return first_fit(
        items_copy,
        capacity
    )


def proposed_method(
    items,
    capacity,
    iterations=1000
):

    best_solution = None
    best_bins = float("inf")

    for _ in range(iterations):

        solution = randomized_ffd(
            items,
            capacity
        )

        bins_used = len(solution)

        if bins_used < best_bins:

            best_bins = bins_used
            best_solution = solution

    return best_solution