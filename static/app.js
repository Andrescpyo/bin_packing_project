// Global variables
let resultsData = [];
let summaryData = [];
let charts = {};

// API calls
async function fetchResults() {
    try {
        const response = await fetch('/api/results');
        if (!response.ok) throw new Error('No results found');
        resultsData = await response.json();
        return resultsData;
    } catch (error) {
        console.error('Error fetching results:', error);
        return [];
    }
}

async function fetchSummary() {
    try {
        const response = await fetch('/api/summary');
        if (!response.ok) throw new Error('No summary found');
        summaryData = await response.json();
        return summaryData;
    } catch (error) {
        console.error('Error fetching summary:', error);
        return [];
    }
}

async function fetchInstances() {
    try {
        const response = await fetch('/api/instances');
        const instances = await response.json();
        return instances;
    } catch (error) {
        console.error('Error fetching instances:', error);
        return [];
    }
}

async function fetchAlgorithms() {
    try {
        const response = await fetch('/api/algorithms');
        const algorithms = await response.json();
        return algorithms;
    } catch (error) {
        console.error('Error fetching algorithms:', error);
        return [];
    }
}

// Navigation
document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const section = item.dataset.section;
        
        // Update active state
        document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        
        // Show section
        document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
        document.getElementById(section).classList.remove('hidden');
        
        // Load data for section
        if (section === 'comparison') {
            loadComparisonCharts();
        } else if (section === 'data') {
            loadDataTable();
        }
    });
});

// Dashboard KPIs
function updateKPIs() {
    if (summaryData.length === 0) return;
    
    const bestByGap = summaryData.reduce((a, b) => a['Avg Gap (%)'] < b['Avg Gap (%)'] ? a : b);
    const bestByOptimal = summaryData.reduce((a, b) => a['Optimal Solutions'] > b['Optimal Solutions'] ? a : b);
    
    document.getElementById('best-algorithm').textContent = bestByGap.Method;
    document.getElementById('avg-gap').textContent = bestByGap['Avg Gap (%)'] + '%';
    document.getElementById('avg-time').textContent = bestByGap['Avg Time (s)'].toFixed(4) + 's';
    document.getElementById('optimal-solutions').textContent = bestByOptimal['Optimal Solutions'];
}

// Charts
function createGapChart() {
    const ctx = document.getElementById('gapChart').getContext('2d');
    
    if (charts.gap) charts.gap.destroy();
    
    charts.gap = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: summaryData.map(d => d.Method),
            datasets: [{
                label: 'Gap Promedio (%)',
                data: summaryData.map(d => d['Avg Gap (%)']),
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(249, 115, 22, 0.8)'
                ],
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(34, 197, 94, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(168, 85, 247, 1)',
                    'rgba(249, 115, 22, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createTimeChart() {
    const ctx = document.getElementById('timeChart').getContext('2d');
    
    if (charts.time) charts.time.destroy();
    
    charts.time = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: summaryData.map(d => d.Method),
            datasets: [{
                label: 'Tiempo Promedio (s)',
                data: summaryData.map(d => d['Avg Time (s)']),
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(249, 115, 22, 0.8)'
                ],
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(34, 197, 94, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(168, 85, 247, 1)',
                    'rgba(249, 115, 22, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createOptimalChart() {
    const ctx = document.getElementById('optimalChart').getContext('2d');
    
    if (charts.optimal) charts.optimal.destroy();
    
    charts.optimal = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: summaryData.map(d => d.Method),
            datasets: [{
                label: 'Soluciones Óptimas',
                data: summaryData.map(d => d['Optimal Solutions']),
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(249, 115, 22, 0.8)'
                ],
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(34, 197, 94, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(168, 85, 247, 1)',
                    'rgba(249, 115, 22, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createRadarChart() {
    const ctx = document.getElementById('radarChart').getContext('2d');
    
    if (charts.radar) charts.radar.destroy();
    
    // Normalize data for radar chart
    const maxGap = Math.max(...summaryData.map(d => d['Avg Gap (%)']));
    const maxTime = Math.max(...summaryData.map(d => d['Avg Time (s)']));
    const maxOptimal = Math.max(...summaryData.map(d => d['Optimal Solutions']));
    
    const datasets = summaryData.map((d, i) => ({
        label: d.Method,
        data: [
            (1 - d['Avg Gap (%)'] / maxGap) * 100,
            (1 - d['Avg Time (s)'] / maxTime) * 100,
            (d['Optimal Solutions'] / maxOptimal) * 100
        ],
        backgroundColor: [
            'rgba(239, 68, 68, 0.2)',
            'rgba(34, 197, 94, 0.2)',
            'rgba(59, 130, 246, 0.2)',
            'rgba(168, 85, 247, 0.2)',
            'rgba(249, 115, 22, 0.2)'
        ][i],
        borderColor: [
            'rgba(239, 68, 68, 1)',
            'rgba(34, 197, 94, 1)',
            'rgba(59, 130, 246, 1)',
            'rgba(168, 85, 247, 1)',
            'rgba(249, 115, 22, 1)'
        ][i],
        borderWidth: 2
    }));
    
    charts.radar = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Calidad (Gap)', 'Velocidad (Tiempo)', 'Precisión (Óptimos)'],
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function loadComparisonCharts() {
    if (resultsData.length === 0) return;
    
    const algorithms = ['NF', 'FF', 'BF', 'FFD', 'PROP'];
    const instances = resultsData.map(d => d.Instance);
    
    // Gap comparison chart
    const gapCtx = document.getElementById('comparisonGapChart').getContext('2d');
    if (charts.comparisonGap) charts.comparisonGap.destroy();
    
    charts.comparisonGap = new Chart(gapCtx, {
        type: 'line',
        data: {
            labels: instances,
            datasets: algorithms.map((alg, i) => ({
                label: alg,
                data: resultsData.map(d => d[`${alg}_gap`]),
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(34, 197, 94, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(168, 85, 247, 1)',
                    'rgba(249, 115, 22, 1)'
                ][i],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.1)',
                    'rgba(34, 197, 94, 0.1)',
                    'rgba(59, 130, 246, 0.1)',
                    'rgba(168, 85, 247, 0.1)',
                    'rgba(249, 115, 22, 0.1)'
                ][i],
                tension: 0.1
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
    
    // Time comparison chart
    const timeCtx = document.getElementById('comparisonTimeChart').getContext('2d');
    if (charts.comparisonTime) charts.comparisonTime.destroy();
    
    charts.comparisonTime = new Chart(timeCtx, {
        type: 'line',
        data: {
            labels: instances,
            datasets: algorithms.map((alg, i) => ({
                label: alg,
                data: resultsData.map(d => d[`${alg}_time`]),
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(34, 197, 94, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(168, 85, 247, 1)',
                    'rgba(249, 115, 22, 1)'
                ][i],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.1)',
                    'rgba(34, 197, 94, 0.1)',
                    'rgba(59, 130, 246, 0.1)',
                    'rgba(168, 85, 247, 0.1)',
                    'rgba(249, 115, 22, 0.1)'
                ][i],
                tension: 0.1
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Data table
function loadDataTable() {
    const tbody = document.getElementById('results-body');
    tbody.innerHTML = '';
    
    resultsData.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-gray-50';
        tr.innerHTML = `
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">${row.Instance}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.Optimal}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.NF}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.NF_gap}%</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.FF}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.FF_gap}%</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.BF}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.BF_gap}%</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.FFD}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.FFD_gap}%</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.PROP}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${row.PROP_gap}%</td>
        `;
        tbody.appendChild(tr);
    });
}

// Search functionality
document.getElementById('search-input').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#results-body tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});

// Export CSV
document.getElementById('export-csv').addEventListener('click', () => {
    const csv = [
        Object.keys(resultsData[0]).join(','),
        ...resultsData.map(row => Object.values(row).join(','))
    ].join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'results_export.csv';
    a.click();
});

// Execution panel
async function loadExecutionPanel() {
    const instances = await fetchInstances();
    const algorithms = await fetchAlgorithms();
    
    // Load instances
    const instancesList = document.getElementById('instances-list');
    instancesList.innerHTML = '';
    instances.forEach(inst => {
        const div = document.createElement('div');
        div.className = 'flex items-center gap-2 p-2 hover:bg-gray-50 rounded';
        div.innerHTML = `
            <input type="checkbox" class="instance-checkbox w-4 h-4 text-blue-600 rounded" value="${inst.name}" checked>
            <span class="text-sm text-gray-700">${inst.name}</span>
            <span class="text-xs text-gray-400 ml-auto">${inst.optimal ? `Óptimo: ${inst.optimal}` : ''}</span>
        `;
        instancesList.appendChild(div);
    });
    
    // Load algorithms
    const algorithmsList = document.getElementById('algorithms-list');
    algorithmsList.innerHTML = '';
    algorithms.forEach(alg => {
        const div = document.createElement('div');
        div.className = 'flex items-center gap-2 p-2 hover:bg-gray-50 rounded';
        div.innerHTML = `
            <input type="checkbox" class="algorithm-checkbox w-4 h-4 text-blue-600 rounded" value="${alg}" checked>
            <span class="text-sm text-gray-700">${alg}</span>
        `;
        algorithmsList.appendChild(div);
    });
    
    // Select all / Deselect all
    document.getElementById('select-all-instances').addEventListener('click', () => {
        document.querySelectorAll('.instance-checkbox').forEach(cb => cb.checked = true);
    });
    
    document.getElementById('deselect-all-instances').addEventListener('click', () => {
        document.querySelectorAll('.instance-checkbox').forEach(cb => cb.checked = false);
    });
}

// Run experiments
document.getElementById('run-experiments').addEventListener('click', async () => {
    const selectedInstances = Array.from(document.querySelectorAll('.instance-checkbox:checked')).map(cb => cb.value);
    const selectedAlgorithms = Array.from(document.querySelectorAll('.algorithm-checkbox:checked')).map(cb => cb.value);
    
    if (selectedInstances.length === 0 || selectedAlgorithms.length === 0) {
        alert('Por favor selecciona al menos una instancia y un algoritmo');
        return;
    }
    
    const statusDiv = document.getElementById('execution-status');
    statusDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/run-experiments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                instances: selectedInstances,
                algorithms: selectedAlgorithms
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            resultsData = result.results;
            summaryData = result.summary;
            updateKPIs();
            createGapChart();
            createTimeChart();
            createOptimalChart();
            createRadarChart();
            alert('Experimentos completados exitosamente');
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error al ejecutar experimentos: ' + error.message);
    } finally {
        statusDiv.classList.add('hidden');
    }
});

// Initialize
async function init() {
    await fetchResults();
    await fetchSummary();
    
    if (resultsData.length > 0 && summaryData.length > 0) {
        updateKPIs();
        createGapChart();
        createTimeChart();
        createOptimalChart();
        createRadarChart();
    }
    
    loadExecutionPanel();
}

init();
