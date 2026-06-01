"""
---
Project: Bin Packing Algorithm Analysis
Author: Andrés Cerdas Padilla
GitHub: https://github.com/Andrescpyo

Description:
Instance reader for bin packing benchmark files.
Parses text files containing bin packing problem instances.
---

Module: instance_reader
"""


class BinPackingInstance:
    """
    Data structure representing a bin packing problem instance.

    Attributes:
        capacity (int): Maximum capacity of each bin.
        items (list): List of item sizes to pack.
        n (int): Number of items.
    """

    def __init__(self, capacity, items):
        """
        Initialize a bin packing instance.

        Args:
            capacity (int): Maximum capacity of each bin.
            items (list): List of item sizes to pack.
        """
        self.capacity = capacity
        self.items = items
        self.n = len(items)


def read_instance(filepath):
    """
    Read a bin packing instance from a text file.

    Expected file format:
    Line 1: Number of items (n)
    Line 2: Bin capacity
    Lines 3+: Item sizes (one per line)

    Args:
        filepath (str): Path to the instance file.

    Returns:
        BinPackingInstance: Parsed instance with capacity and items.

    Raises:
        ValueError: If the number of items read doesn't match the declared count.
    """
    with open(filepath, "r") as f:
        lines = [int(line.strip()) for line in f if line.strip()]

    n = lines[0]
    capacity = lines[1]
    items = lines[2:]

    if len(items) != n:
        raise ValueError(
            f"Se esperaban {n} objetos y se encontraron {len(items)}"
        )

    return BinPackingInstance(capacity, items)