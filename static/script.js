document.getElementById('article-form').addEventListener('submit', function(event) {
    var articleLink = document.getElementById('article_link').value;
    if (!articleLink) {
        event.preventDefault();
        alert('Please enter an article link.');
    } else if (!/^https?:\/\//i.test(articleLink)) {
        event.preventDefault();
        alert('Please enter a valid URL. It should start with "http://" or "https://".');
    }
});

// Fetch the scores from the server
fetch('/get_scores')
    .then(response => response.json())
    .then(scores => {
        let labels = Object.keys(scores);
        let data = Object.values(scores);

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