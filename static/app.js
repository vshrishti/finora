document.addEventListener('DOMContentLoaded', () => {
    init();
    setupModal();
});

function setupModal() {
    const modal = document.getElementById('txModal');
    if (!modal) return;
    const modalContent = modal.querySelector('div');
    const btn = document.getElementById('addTxBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const form = document.getElementById('txForm');
    
    // Set default date to today
    document.getElementById('txDate').valueAsDate = new Date();

    const openModal = () => {
        modal.classList.remove('hidden');
        setTimeout(() => {
            modal.classList.remove('opacity-0');
            modalContent.classList.remove('scale-95');
        }, 10);
    };

    const closeModal = () => {
        modal.classList.add('opacity-0');
        modalContent.classList.add('scale-95');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
    };

    if (btn) btn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btnSubmit = form.querySelector('button[type="submit"]');
            btnSubmit.innerHTML = 'Saving...';
            
            const txData = {
                transaction_date: document.getElementById('txDate').value,
                transaction_type: document.getElementById('txType').value,
                amount: parseFloat(document.getElementById('txAmount').value),
                category: document.getElementById('txCategory').value,
                description: document.getElementById('txDesc').value,
                payment_method: 'Cash'
            };

            const res = await fetch('/api/transactions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(txData)
            });

            if (res.ok) {
                closeModal();
                form.reset();
                document.getElementById('txDate').valueAsDate = new Date();
                await init(); // Refresh dashboard
            }
            btnSubmit.innerHTML = 'Save Transaction';
        });
    }
}

const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
};

let trendChartInst = null;
let catChartInst = null;

async function init() {
    await fetchMetrics();
    await fetchTransactions();
    await renderCharts();

    document.getElementById('loadDemoBtn').addEventListener('click', async () => {
        const btn = document.getElementById('loadDemoBtn');
        const origText = btn.innerHTML;
        btn.innerHTML = '⏳ Loading...';
        await fetch('/api/demo', { method: 'POST' });
        await init();
        btn.innerHTML = origText;
    });
}

async function fetchMetrics() {
    const res = await fetch('/api/metrics');
    const data = await res.json();
    
    document.getElementById('valIncome').innerText = formatCurrency(data.total_income);
    document.getElementById('valExpense').innerText = formatCurrency(data.total_expenses);
    document.getElementById('valSavings').innerText = formatCurrency(data.savings);
    document.getElementById('valRate').innerText = `${data.savings_rate}%`;
    document.getElementById('rateBar').style.width = `${Math.min(data.savings_rate, 100)}%`;
}

async function fetchTransactions() {
    const res = await fetch('/api/transactions');
    const data = await res.json();
    
    const tbody = document.getElementById('txTableBody');
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="px-6 py-8 text-center text-slate-400">No transactions found. Load demo data to explore.</td></tr>`;
        return;
    }

    data.slice(0, 10).forEach(tx => {
        const tr = document.createElement('tr');
        const isExpense = tx.transaction_type === 'Expense';
        const typeBadge = isExpense 
            ? `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-rose-100 text-rose-800">Expense</span>`
            : `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800">Income</span>`;
            
        const amountClass = isExpense ? 'text-slate-800' : 'text-emerald-600 font-semibold';
        
        tr.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-slate-600">${tx.transaction_date}</td>
            <td class="px-6 py-4 whitespace-nowrap">${typeBadge}</td>
            <td class="px-6 py-4 whitespace-nowrap"><span class="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg text-xs font-medium">${tx.category}</span></td>
            <td class="px-6 py-4 whitespace-nowrap text-slate-500">${tx.description || '-'}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right ${amountClass}">${isExpense ? '-' : '+'}${formatCurrency(tx.amount)}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function renderCharts() {
    Chart.defaults.font.family = "'Outfit', sans-serif";
    Chart.defaults.color = '#64748b';

    // Fetch Trend
    const trendRes = await fetch('/api/charts/trend');
    const trendData = await trendRes.json();
    
    const ctxTrend = document.getElementById('trendChart').getContext('2d');
    if (trendChartInst) trendChartInst.destroy();
    
    const gradient = ctxTrend.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(16, 185, 129, 0.2)');
    gradient.addColorStop(1, 'rgba(16, 185, 129, 0)');

    trendChartInst = new Chart(ctxTrend, {
        type: 'line',
        data: {
            labels: trendData.labels,
            datasets: [{
                label: 'Daily Spending',
                data: trendData.values,
                borderColor: '#10b981',
                backgroundColor: gradient,
                borderWidth: 2,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#10b981',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleFont: { size: 13 },
                    bodyFont: { size: 14, weight: 'bold' },
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return formatCurrency(context.raw);
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false, drawBorder: false }
                },
                y: {
                    grid: { color: '#f1f5f9', drawBorder: false },
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000) return '₹' + (value / 1000) + 'k';
                            return '₹' + value;
                        }
                    }
                }
            }
        }
    });

    // Fetch Category
    const catRes = await fetch('/api/charts/category');
    const catData = await catRes.json();
    
    const ctxCat = document.getElementById('categoryChart').getContext('2d');
    if (catChartInst) catChartInst.destroy();
    
    catChartInst = new Chart(ctxCat, {
        type: 'doughnut',
        data: {
            labels: catData.labels,
            datasets: [{
                data: catData.values,
                backgroundColor: [
                    '#10b981', '#3b82f6', '#f43f5e', '#f59e0b', 
                    '#8b5cf6', '#06b6d4', '#ec4899', '#64748b'
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return ' ' + formatCurrency(context.raw);
                        }
                    }
                }
            }
        }
    });
}
