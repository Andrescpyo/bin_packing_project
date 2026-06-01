"""
---
Project: Bin Packing Algorithm Analysis
Author: Andrés Cerdas Padilla
GitHub: https://github.com/Andrescpyo

Description:
Results analysis module for bin packing experiments.
Computes summary statistics and rankings for algorithm performance.
---

Module: analyze_results
"""

import pandas as pd


def main():
    """
    Analyze experiment results and generate summary statistics.

    Reads results.csv, computes average gap, time, and optimal solution counts
    for each algorithm, then prints rankings and best performers.
    Saves summary to summary.csv.

    Side effects:
        - Prints analysis results to console
        - Creates summary.csv file
    """
    try:
        df = pd.read_csv("results\\results.csv")

    except FileNotFoundError:
        print("ERROR: No se encontró results.csv")
        return

    methods = ["NF", "FF", "BF", "FFD", "PROP"]

    summary = []

    print("\n" + "=" * 60)
    print("RESULTADOS GLOBALES")
    print("=" * 60)

    for method in methods:

        avg_gap = df[f"{method}_gap"].mean()

        avg_time = df[f"{method}_time"].mean()

        optimal_count = (
            df[method] == df["Optimal"]
        ).sum()

        summary.append([
            method,
            round(avg_gap, 2),
            round(avg_time, 6),
            int(optimal_count)
        ])

    summary_df = pd.DataFrame(
        summary,
        columns=[
            "Method",
            "Avg Gap (%)",
            "Avg Time (s)",
            "Optimal Solutions"
        ]
    )

    print("\nRESUMEN ESTADÍSTICO\n")
    print(summary_df.to_string(index=False))

    summary_df.to_csv(
        "results/summary.csv",
        index=False
    )

    print("\nsummary.csv generado correctamente.")

    # Mejor método por GAP
    best_gap = summary_df.loc[
        summary_df["Avg Gap (%)"].idxmin()
    ]

    print("\n" + "=" * 60)
    print("MEJOR MÉTODO POR GAP PROMEDIO")
    print("=" * 60)

    print(
        f"{best_gap['Method']} "
        f"(Gap promedio = {best_gap['Avg Gap (%)']}%)"
    )

    # Método con más óptimos
    best_optimal = summary_df.loc[
        summary_df["Optimal Solutions"].idxmax()
    ]

    print("\n" + "=" * 60)
    print("MÉTODO CON MÁS SOLUCIONES ÓPTIMAS")
    print("=" * 60)

    print(
        f"{best_optimal['Method']} "
        f"({best_optimal['Optimal Solutions']} óptimos)"
    )

    # Ranking por GAP
    ranking = summary_df.sort_values(
        by="Avg Gap (%)"
    )

    print("\n" + "=" * 60)
    print("RANKING DE MÉTODOS")
    print("=" * 60)

    for pos, (_, row) in enumerate(
        ranking.iterrows(),
        start=1
    ):
        print(
            f"{pos}. {row['Method']} "
            f"(Gap = {row['Avg Gap (%)']}%)"
        )

    print("\nAnálisis finalizado.")


if __name__ == "__main__":
    main()