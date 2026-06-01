# Bin Packing Algorithm Analysis

A comprehensive analysis framework for bin packing algorithms with interactive visualization dashboard. Includes both command-line tools and a standalone executable for easy deployment.

**Author:** Andrés Cerdas Padilla
**GitHub:** https://github.com/Andrescpyo

## Overview

This project implements and analyzes multiple bin packing heuristics on benchmark instances from the Falkenauer dataset. It includes both command-line execution tools and an interactive web dashboard for visualizing results. The application can be run as a Python script or as a standalone executable built with PyInstaller.

## Algorithms Implemented

- **NF (Next Fit)** - Simple online algorithm
- **FF (First Fit)** - Places items in the first bin with sufficient space
- **BF (Best Fit)** - Places items in the bin with the least remaining space
- **FFD (First Fit Decreasing)** - Sorts items descending before applying First Fit
- **PROP (Proposed Method)** - Local search approach with randomized FFD (500 iterations)

## Project Structure

```
bin_packing_project/
├── app.py                      # Flask web server with PyInstaller support
├── main.py                     # Command-line entry point
├── analyze_results.py          # Results analysis script
├── icon.ico                    # Application favicon
├── .gitignore                  # Git ignore rules
├── static/
│   ├── index.html              # Dashboard interface
│   └── app.js                  # Frontend logic
├── src/
│   ├── experiment.py          # Experiment runner with resource_path
│   ├── heuristics.py           # Classic heuristics
│   ├── local_search.py         # Proposed local search
│   └── instance_reader.py      # Instance file parser
├── data/                       # Benchmark instances
│   └── Optimo.txt              # Optimal solution values
├── results/                    # Generated results
│   ├── results.csv
│   ├── results.xlsx
│   └── summary.csv
├── build/                      # PyInstaller build artifacts
├── dist/                       # PyInstaller distribution
└── DASHBOARD_README.md         # Dashboard-specific documentation
```

## Installation

### Development Mode

1. Activate virtual environment:
```powershell
.\bpp_env\Scripts\activate
```

2. Install dependencies:
```powershell
pip install pandas flask openpyxl pyinstaller
```

### Building Executable

To create a standalone executable:

```powershell
pyinstaller --onefile --windowed --icon=icon.ico --add-data "data;data" --add-data "static;static" app.py
```

The executable will be created in the `dist/` folder.

## Usage

### Command Line

Run all experiments:
```powershell
python main.py
```

Analyze results:
```powershell
python analyze_results.py
```

### Web Dashboard (Development)

Start the Flask server:
```powershell
python app.py
```

The dashboard will automatically open in your default browser at `http://127.0.0.1:5000`

### Web Dashboard (Executable)

Run the standalone executable:
```powershell
.\dist\app.exe
```

The dashboard will automatically open in your default browser at `http://127.0.0.1:5000`

See [DASHBOARD_README.md](DASHBOARD_README.md) for detailed dashboard usage.

## Data Format

### Instance Files

Text files with the following format:
```
<number of items>
<bin capacity>
<item size 1>
<item size 2>
...
```

### Optimal Values File

Tab-separated file mapping instance names to optimal bin counts:
```
Falkenauer_u120_00.txt	48
Falkenauer_u120_01.txt	49
...
```

## Output Files

All output files are stored in the `results/` folder:

- `results/results.csv` - Detailed results for each instance and algorithm
- `results/results.xlsx` - Excel format of results
- `results/summary.csv` - Statistical summary by algorithm

## Metrics

For each algorithm, the following metrics are computed:

- **Bins Used** - Number of bins in the solution
- **Execution Time** - Time taken to compute the solution (seconds)
- **Gap (%)** - Percentage deviation from optimal solution: `(bins - optimal) / optimal * 100`

## Technologies

- **Python 3.x**
- **Pandas** - Data processing
- **Flask** - Web server
- **Chart.js** - Visualization
- **TailwindCSS** - Styling
- **PyInstaller** - Executable packaging

## Benchmark Instances

The project uses Falkenauer benchmark instances:
- **u120/u250/u500/u1000** - Uniform distribution instances
- **t60/t120/t249/t501** - Triplets distribution instances

## Features

- **PyInstaller Compatibility**: Application can be packaged as standalone executable
- **Resource Path Handling**: Automatic path resolution for development and packaged modes
- **Auto Browser Launch**: Dashboard automatically opens in default browser
- **Custom Favicon**: Application icon displayed in browser tab
- **Single Results Folder**: All results stored in unified `results/` directory

## License

This project is for educational and research purposes.
