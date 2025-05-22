fetch('/grafici').then(res => res.json()).then(data => {
    const ctx = document.getElementById('graficoMeteo').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Temperatura (°C)',
                data: data.temperatura,
                fill: false,
                borderColor: 'blue',
                tension: 0.1
            }]
        }
    });
});
