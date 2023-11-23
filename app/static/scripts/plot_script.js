// app/static/scripts/plot_script.js
document.addEventListener('DOMContentLoaded', function() {
    console.log("Chart.js Loaded");

    // Fetch data from the server and update the plot
    function updatePlot() {
        fetch('/get_latest_data')
            .then(response => response.json())
            .then(data => {
                console.log("Data:", data);
                createPlot(data);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }

    // Create simple plot
    function createPlot(data) {
        const plotContainer = document.getElementById('plot');
        plotContainer.innerHTML = ''; // Clear previous content

        const canvas = document.createElement('canvas');
        canvas.id = 'myChart';
        plotContainer.appendChild(canvas);

        const ctx = canvas.getContext('2d');

        const dates = data.map(entry => entry.DateTime);
        const values = data.map(entry => entry.Value);
        const anomalies = data.map(entry => entry.Anomaly);

        // Filter indices of anomaly points where value is 1 or -1
        const anomalyIndices = anomalies.reduce((acc, anomaly, index) => {
            if (anomaly ==-1) {
                acc.push(index);
            }
            return acc;
        }, []);

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Data Stream',
                        borderColor: 'blue',
                        data: values,
                        fill: false,
                    },
                    {
                        label: 'Anomalies',
                        borderColor: 'transparent',
                        // backgroundColor: 'red',
                        pointRadius: 8,
                        pointHoverRadius: 12,
                        pointBackgroundColor: 'red',
                        pointBorderColor: 'red',
                        pointBorderWidth: 1,
                        data: anomalyIndices.map(index => ({ x: dates[index], y: values[index] })),
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                        },
                    },
                    y: {
                        beginAtZero: true,
                    },
                },
                animation: {
                    duration: 10, // Animation duration in milliseconds
                    easing: 'linear', // Easing function (e.g., 'linear', 'easeInOutCubic')
                    onComplete: (animation) => {
                        // Trigger the next update when the animation is complete
                        // Periodically update the plot every 1 second
                        setInterval(updatePlot, 1000);
                        updatePlot();
                    },
                },
            },
        });
    }


    // Initial plot update
    updatePlot();

    // // Periodically update the plot every 1 second
    // setInterval(updatePlot, 100);

    // // Initial plot update
    // updatePlot();
});
