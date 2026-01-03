/**
 * GritCoin Dashboard Charts
 * Handles dynamic chart rendering with Chart.js
 */

// Chart instances (global to allow updates)
let studyChart = null;
let expenseChart = null;

// Current selected period
let currentPeriod = 'week';

/**
 * Fetch chart data from the backend API
 * @param {string} period - 'week', 'month', or 'quarter'
 * @returns {Promise<Array>} Chart data
 */
async function fetchChartData(period) {
    try {
        const response = await fetch(`/dashboard/chart-data/${period}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching chart data:', error);
        alert('Failed to load chart data. Please refresh the page.');
        return [];
    }
}

/**
 * Create or update the study time chart
 * @param {Array} data - Chart data from API
 */
function renderStudyChart(data) {
    const ctx = document.getElementById('studyChart').getContext('2d');
    
    // Extract labels and values
    const labels = data.map(item => {
        const date = new Date(item.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const values = data.map(item => item.study);
    
    // Destroy existing chart if it exists
    if (studyChart) {
        studyChart.destroy();
    }
    
    // Create new chart
    studyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Study Time (minutes)',
                data: values,
                backgroundColor: 'rgba(13, 110, 253, 0.6)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 30
                    },
                    title: {
                        display: true,
                        text: 'Minutes'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + ' min';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create or update the expenses chart
 * @param {Array} data - Chart data from API
 */
function renderExpenseChart(data) {
    const ctx = document.getElementById('expenseChart').getContext('2d');
    
    // Extract labels and values
    const labels = data.map(item => {
        const date = new Date(item.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const values = data.map(item => item.expense);
    
    // Destroy existing chart if it exists
    if (expenseChart) {
        expenseChart.destroy();
    }
    
    // Create new chart
    expenseChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses ($)',
                data: values,
                backgroundColor: 'rgba(25, 135, 84, 0.6)',
                borderColor: 'rgba(25, 135, 84, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Amount ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

/**
 * Load and render charts for the selected period
 * @param {string} period - 'week', 'month', or 'quarter'
 */
async function loadCharts(period) {
    currentPeriod = period;
    
    // Fetch data
    const data = await fetchChartData(period);
    
    // Render both charts
    if (data.length > 0) {
        renderStudyChart(data);
        renderExpenseChart(data);
    } else {
        // Handle empty data
        console.warn('No data available for the selected period');
    }
}

/**
 * Initialize dashboard on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Load initial charts (weekly by default)
    loadCharts('week');
    
    // Add event listeners to period selector buttons
    const periodButtons = document.querySelectorAll('input[name="period"]');
    periodButtons.forEach(button => {
        button.addEventListener('change', function() {
            if (this.checked) {
                loadCharts(this.value);
            }
        });
    });
});