"""
---
Project: Bin Packing Algorithm Analysis
Author: Andrés Cerdas Padilla
GitHub: https://github.com/Andrescpyo

Description:
Local search algorithm for bin packing optimization.
Implements a randomized First Fit Decreasing approach with iterative improvement.
---

Module: local_search
"""

import random

from src.heuristics import first_fit


def randomized_ffd(items, capacity):
    """
    Randomized First Fit Decreasing algorithm.

    Sorts items in descending order, performs random swaps to introduce variation,
    then applies First Fit. Used as a subroutine for the proposed method.

    Args:
        items (list): List of item sizes to pack.
        capacity (int): Maximum capacity of each bin.

    Returns:
        list: List of bins, where each bin is a list of item sizes.
    """
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
    iterations=500
):
    """
    Proposed local search method for bin packing.

    Iteratively applies randomized FFD and keeps the best solution found.
    Uses randomization to escape local optima and explore the solution space.

    Args:
        items (list): List of item sizes to pack.
        capacity (int): Maximum capacity of each bin.
        iterations (int): Number of randomized FFD iterations to perform.
                         Default is 1000.

    Returns:
        list: Best solution found (list of bins, where each bin is a list of item sizes).
    """
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