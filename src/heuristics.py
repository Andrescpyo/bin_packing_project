def next_fit(items, capacity):
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

    sorted_items = sorted(items, reverse=True)

    return first_fit(sorted_items, capacity)