class BinPackingInstance:

    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.n = len(items)


def read_instance(filepath):

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