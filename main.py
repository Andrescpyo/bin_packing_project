"""
---
Project: Bin Packing Algorithm Analysis
Author: Andrés Cerdas Padilla
GitHub: https://github.com/Andrescpyo

Description:
Main entry point for running bin packing experiments across all defined instances.
Executes all algorithms and generates results in CSV and Excel formats.
---
"""

from src.experiment import run_experiments


def main():
    """Run all bin packing experiments and display results."""
    df = run_experiments()

    print("\nRESULTADOS\n")

    print(df)


if __name__ == "__main__":
    main()