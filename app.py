from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import os
from src.experiment import ALGORITHMS
from src.instance_reader import read_instance


def load_optimal_values():
    """Load optimal values from Optimo.txt file."""
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
    return send_from_directory('static', 'index.html')

@app.route('/api/results')
def get_results():
    try:
        df = pd.read_csv('results/results.csv')
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify({'error': 'No results found. Run experiments first.'}), 404

@app.route('/api/summary')
def get_summary():
    try:
        df = pd.read_csv('summary.csv')
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify({'error': 'No summary found. Run experiments first.'}), 404

@app.route('/api/instances')
def get_instances():
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
    return jsonify(list(ALGORITHMS.keys()))

@app.route('/api/run-experiments', methods=['POST'])
def run_experiments_api():
    try:
        data = request.json
        selected_instances = data.get('instances', list(OPTIMAL.keys()))
        selected_algorithms = data.get('algorithms', list(ALGORITHMS.keys()))
        
        # Modify experiment to run only selected instances and algorithms
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
                    
                import time
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
        
        # Generate summary
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
