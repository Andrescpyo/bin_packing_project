"""
---
Project: Bin Packing Algorithm Analysis
Author: Andrés Cerdas Padilla
GitHub: https://github.com/Andrescpyo

Description:
Experiment runner module for bin packing algorithms.
Executes multiple heuristics on benchmark instances and collects performance metrics.
---

Module: experiment
"""

import os
import time
import pandas as pd

from src.instance_reader import read_instance

from src.heuristics import (
    next_fit,
    first_fit,
    best_fit,
    first_fit_decreasing
)

from src.local_search import proposed_method


def load_optimal_values():
    """
    Load optimal values from Optimo.txt file.

    Reads a tab-separated file containing instance names and their optimal bin counts.
    Format: filename.txt<TAB>optimal_value

    Returns:
        dict: Mapping of filename to optimal bin count.
    """
    optimal = {}
    try:
        with open(os.path.join("data", "Optimo.txt"), "r") as f:
            for line in f:
                line = line.strip()
                if line and "\t" in line:
                    parts = line.split("\t")
                    filename = parts[0].strip()
                    value = int(parts[1].strip())
                    optimal[filename] = value
    except FileNotFoundError:
        print("Warning: Optimo.txt not found, using empty optimal values")
    return optimal


OPTIMAL = load_optimal_values()

ALGORITHMS = {
    "NF": next_fit,
    "FF": first_fit,
    "BF": best_fit,
    "FFD": first_fit_decreasing,
    "PROP": proposed_method
}


def run_experiments():
    """
    Run all bin packing algorithms on defined instances.

    For each instance in OPTIMAL, executes all algorithms and records:
    - Number of bins used
    - Execution time
    - Gap percentage from optimal solution

    Results are saved to results/results.csv and results/results.xlsx.

    Returns:
        pd.DataFrame: DataFrame containing results for all instances and algorithms.
    """
    results = []

    for filename in OPTIMAL:

        print(f"Procesando {filename}")

        instance = read_instance(
            os.path.join("data", filename)
        )

        row = {
            "Instance": filename,
            "Optimal": OPTIMAL[filename]
        }

        for name, algorithm in ALGORITHMS.items():

            start = time.perf_counter()

            solution = algorithm(
                instance.items,
                instance.capacity
            )

            elapsed = time.perf_counter() - start

            bins_used = len(solution)

            row[name] = bins_used
            row[f"{name}_time"] = elapsed

            row[f"{name}_gap"] = round(
                (
                    bins_used - OPTIMAL[filename]
                )
                / OPTIMAL[filename]
                * 100,
                2
            )

        results.append(row)

    df = pd.DataFrame(results)

    os.makedirs("results", exist_ok=True)

    df.to_csv(
        "results/results.csv",
        index=False
    )

    df.to_excel(
        "results/results.xlsx",
        index=False
    )

    return df