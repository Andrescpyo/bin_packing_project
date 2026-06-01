"""
---
Project: Bin Packing Algorithm Analysis
Author: Andrés Cerdas Padilla
GitHub: https://github.com/Andrescpyo

Description:
Classic bin packing heuristic algorithms.
Implements Next Fit, First Fit, Best Fit, and First Fit Decreasing strategies.
---

Module: heuristics
"""


def next_fit(items, capacity):
    """
    Next Fit algorithm for bin packing.

    Places each item in the current bin if it fits, otherwise closes the current
    bin and opens a new one. Simple but often suboptimal.

    Args:
        items (list): List of item sizes to pack.
        capacity (int): Maximum capacity of each bin.

    Returns:
        list: List of bins, where each bin is a list of item sizes.
    """
    bins = []
    current_bin = []
    remaining = capacity

    for item in items:

        if item <= remaining:
            current_bin.append(item)
            remaining -= item

        else:
            bins.append(current_bin)

            current_bin = [item]
            remaining = capacity - item

    if current_bin:
        bins.append(current_bin)

    return bins


def first_fit(items, capacity):
    """
    First Fit algorithm for bin packing.

    Places each item in the first bin that has enough remaining capacity.
    If no existing bin can accommodate the item, opens a new bin.

    Args:
        items (list): List of item sizes to pack.
        capacity (int): Maximum capacity of each bin.

    Returns:
        list: List of bins, where each bin is a list of item sizes.
    """
    bins = []

    for item in items:

        placed = False

        for b in bins:

            if sum(b) + item <= capacity:
                b.append(item)
                placed = True
                break

        if not placed:
            bins.append([item])

    return bins


def best_fit(items, capacity):
    """
    Best Fit algorithm for bin packing.

    Places each item in the bin that will have the least remaining space
    after placement. Tends to produce better packing than First Fit.

    Args:
        items (list): List of item sizes to pack.
        capacity (int): Maximum capacity of each bin.

    Returns:
        list: List of bins, where each bin is a list of item sizes.
    """
    bins = []

    for item in items:

        best_bin_index = -1
        smallest_remaining = float("inf")

        for i, b in enumerate(bins):

            free_space = capacity - sum(b)

            if item <= free_space:

                remaining_after = free_space - item

                if remaining_after < smallest_remaining:
                    smallest_remaining = remaining_after
                    best_bin_index = i

        if best_bin_index == -1:
            bins.append([item])
        else:
            bins[best_bin_index].append(item)

    return bins


def first_fit_decreasing(items, capacity):
    """
    First Fit Decreasing algorithm for bin packing.

    Sorts items in descending order before applying First Fit.
    Sorting larger items first typically improves solution quality.

    Args:
        items (list): List of item sizes to pack.
        capacity (int): Maximum capacity of each bin.

    Returns:
        list: List of bins, where each bin is a list of item sizes.
    """
    sorted_items = sorted(items, reverse=True)

    return first_fit(sorted_items, capacity)