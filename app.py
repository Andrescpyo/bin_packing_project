"""
---
Project: Bin Packing Algorithm Analysis
Author: Andrés Cerdas Padilla
GitHub: https://github.com/Andrescpyo

Description:
Flask web server providing REST API for bin packing experiments and results visualization.
Serves the interactive dashboard and handles experiment execution requests.
---

Module: app
"""

from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import os
import time
from src.experiment import ALGORITHMS
from src.instance_reader import read_instance


def load_optimal_values():
    """
    Load optimal values from Optimo.txt file.

    Reads a tab-separated file containing instance names and their optimal bin counts.

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

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def index():
    """
    Serve the main dashboard page.

    Returns:
        FileResponse: The index.html file from the static folder.
    """
    return send_from_directory('static', 'index.html')


@app.route('/api/results')
def get_results():
    """
    Get detailed experiment results.

    Returns:
        JSON: Array of result objects with metrics for each instance and algorithm.
              Returns 404 if results file doesn't exist.
    """
    try:
        df = pd.read_csv('results/results.csv')
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify({'error': 'No results found. Run experiments first.'}), 404


@app.route('/api/summary')
def get_summary():
    """
    Get summary statistics for all algorithms.

    Returns:
        JSON: Array of summary objects with average gap, time, and optimal solution counts.
              Returns 404 if summary file doesn't exist.
    """
    try:
        df = pd.read_csv('results/summary.csv')
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify({'error': 'No summary found. Run experiments first.'}), 404


@app.route('/api/instances')
def get_instances():
    """
    Get list of available instance files.

    Scans the data directory for .txt files and returns metadata including
    file size and optimal value if known.

    Returns:
        JSON: Array of instance objects with name, size, and optimal value.
    """
    instances = []
    for filename in os.listdir('data'):
        if filename.endswith('.txt'):
            filepath = os.path.join('data', filename)
            size = os.path.getsize(filepath)
            instances.append({
                'name': filename,
                'size': size,
                'optimal': OPTIMAL.get(filename, None)
            })
    return jsonify(instances)


@app.route('/api/algorithms')
def get_algorithms():
    """
    Get list of available algorithms.

    Returns:
        JSON: Array of algorithm names (e.g., ['NF', 'FF', 'BF', 'FFD', 'PROP']).
    """
    return jsonify(list(ALGORITHMS.keys()))


@app.route('/api/run-experiments', methods=['POST'])
def run_experiments_api():
    """
    Run bin packing experiments on selected instances and algorithms.

    Request body:
        instances (list): List of instance filenames to process.
        algorithms (list): List of algorithm names to run.

    Returns:
        JSON: Object containing:
            - success (bool): Whether execution succeeded
            - results (list): Detailed results for each instance
            - summary (list): Summary statistics for each algorithm
              Returns 500 on error.
    """
    try:
        data = request.json
        selected_instances = data.get('instances', list(OPTIMAL.keys()))
        selected_algorithms = data.get('algorithms', list(ALGORITHMS.keys()))

        results = []
        for filename in selected_instances:
            if filename not in OPTIMAL:
                continue

            print(f"Processing {filename}")
            instance = read_instance(os.path.join('data', filename))

            row = {
                'Instance': filename,
                'Optimal': OPTIMAL[filename]
            }

            for name, algorithm in ALGORITHMS.items():
                if name not in selected_algorithms:
                    continue

                start = time.perf_counter()
                solution = algorithm(instance.items, instance.capacity)
                elapsed = time.perf_counter() - start
                bins_used = len(solution)

                row[name] = bins_used
                row[f'{name}_time'] = elapsed
                row[f'{name}_gap'] = round((bins_used - OPTIMAL[filename]) / OPTIMAL[filename] * 100, 2)

            results.append(row)

        df = pd.DataFrame(results)
        os.makedirs('results', exist_ok=True)
        df.to_csv('results/results.csv', index=False)
        df.to_excel('results/results.xlsx', index=False)

        methods = selected_algorithms
        summary = []
        for method in methods:
            avg_gap = df[f'{method}_gap'].mean()
            avg_time = df[f'{method}_time'].mean()
            optimal_count = (df[method] == df['Optimal']).sum()
            summary.append({
                'Method': method,
                'Avg Gap (%)': round(avg_gap, 2),
                'Avg Time (s)': round(avg_time, 6),
                'Optimal Solutions': int(optimal_count)
            })

        summary_df = pd.DataFrame(summary)
        summary_df.to_csv('summary.csv', index=False)

        return jsonify({
            'success': True,
            'results': df.to_dict(orient='records'),
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
