// chart.js

// Fetch the scores from the server
fetch('/get_scores')
    .then(response => response.json())
    .then(articleScores => {
        let labels = Object.keys(articleScores);
        let data = Object.values(articleScores);

        // Create the chart
        let ctx = document.getElementById('scoreChart').getContext('2d');
        let myRadarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    // ... other dataset properties
                }]
            },
            options: {
                // ... chart options
            }
        });
    });