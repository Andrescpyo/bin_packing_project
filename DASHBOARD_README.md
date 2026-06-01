# Bin Packing Analysis Dashboard

Interactive web dashboard for visualizing and analyzing bin packing algorithm results.

**Author:** Andrés Cerdas Padilla
**GitHub:** https://github.com/Andrescpyo

## Features

- **Interactive Dashboard** with real-time KPIs and charts
- **Execution Panel** for running custom experiments
- **Algorithm Comparison** with detailed visualizations
- **Data Table** with search, filters, and export functionality
- **Responsive Design** using TailwindCSS

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5 + TailwindCSS (via CDN)
- **Charts:** Chart.js (via CDN)
- **Data Processing:** Pandas

## Installation

1. Activate virtual environment:
```powershell
.\bpp_env\Scripts\activate
```

2. Install Flask (if not already installed):
```powershell
pip install flask
```

## Usage

1. Start the server:
```powershell
python app.py
```

2. Open browser at:
```
http://localhost:5000
```

## Dashboard Sections

### Dashboard
- View main KPIs (best algorithm, average gap, average time, optimal solutions)
- Bar charts for gap and time by algorithm
- Radar chart for multidimensional performance comparison

### Execution
- Select instances to process
- Choose algorithms to execute
- Click "Ejecutar" to run experiments
- Results automatically update in the dashboard

### Comparison
- Line charts comparing gap and time across instances
- Toggle series from chart legend

### Data
- Complete table with all results
- Real-time search
- CSV export

## API Endpoints

- `GET /` - Web interface
- `GET /api/results` - Detailed results
- `GET /api/summary` - Statistical summary
- `GET /api/instances` - List of available instances
- `GET /api/algorithms` - List of available algorithms
- `POST /api/run-experiments` - Run custom experiments

## File Structure

```
bin_packing_project/
├── app.py                      # Flask server
├── static/
│   ├── index.html              # Main interface
│   └── app.js                  # JavaScript logic
├── src/
│   ├── experiment.py          # Experiment logic
│   ├── heuristics.py           # Bin packing algorithms
│   ├── local_search.py         # Local search algorithm
│   └── instance_reader.py      # Instance file reader
├── data/                       # Instance files
├── results/                    # Generated results
└── main.py                     # Original script (unmodified)
```

## Notes

- Algorithm logic remains unchanged
- Original backend (main.py, experiment.py) is intact
- Dashboard is an additional visualization layer
- Results are saved to `results/results.csv` and `summary.csv`
