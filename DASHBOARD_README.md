# Bin Packing Analysis Dashboard

Interfaz visual moderna para el análisis de resultados de algoritmos de Bin Packing.

## Características

- **Dashboard interactivo** con KPIs y gráficos en tiempo real
- **Panel de ejecución** para correr experimentos personalizados
- **Comparación de algoritmos** con visualizaciones detalladas
- **Tabla de datos** con búsqueda, filtros y exportación
- **Diseño responsive** con TailwindCSS

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5 + TailwindCSS (vía CDN)
- **Gráficos**: Chart.js (vía CDN)
- **Procesamiento de datos**: Pandas

## Instalación

1. Activar el entorno virtual:
```powershell
.\bpp_env\Scripts\activate
```

2. Instalar Flask (si no está instalado):
```powershell
pip install flask
```

## Ejecución

1. Iniciar el servidor:
```powershell
python app.py
```

2. Abrir el navegador en:
```
http://localhost:5000
```

## Uso

### Dashboard
- Visualiza KPIs principales (mejor algoritmo, gap promedio, tiempo promedio, soluciones óptimas)
- Gráficos de barras para gap y tiempo por algoritmo
- Gráfico de radar para rendimiento multidimensional

### Ejecución
- Selecciona las instancias que deseas procesar
- Elige los algoritmos a ejecutar
- Click en "Ejecutar" para correr los experimentos
- Los resultados se actualizan automáticamente en el dashboard

### Comparación
- Gráficos de líneas comparando gap y tiempo por instancia
- Activa/desactiva series desde la leyenda del gráfico

### Datos
- Tabla completa con todos los resultados
- Búsqueda en tiempo real
- Exportación a CSV

## API Endpoints

- `GET /` - Interfaz web
- `GET /api/results` - Resultados detallados
- `GET /api/summary` - Resumen estadístico
- `GET /api/instances` - Lista de instancias disponibles
- `GET /api/algorithms` - Lista de algoritmos disponibles
- `POST /api/run-experiments` - Ejecutar experimentos personalizados

## Estructura de Archivos

```
bin_packing_project/
├── app.py                      # Servidor Flask
├── static/
│   ├── index.html              # Interfaz principal
│   └── app.js                  # Lógica JavaScript
├── src/
│   ├── experiment.py          # Lógica de experimentos
│   ├── heuristics.py           # Algoritmos de bin packing
│   ├── local_search.py         # Búsqueda local
│   └── instance_reader.py      # Lector de instancias
├── data/                       # Archivos de instancias
├── results/                    # Resultados generados
└── main.py                     # Script original (sin modificar)
```

## Notas

- No se modificó la lógica de los algoritmos
- El backend original (main.py, experiment.py) permanece intacto
- La interfaz es una capa adicional para visualización
- Los resultados se guardan en `results/results.csv` y `summary.csv`
