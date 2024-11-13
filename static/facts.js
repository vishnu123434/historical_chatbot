
function fetchRandomFact() {
    fetch('/api/random_fact')
        .then(response => response.json())
        .then(data => {
            // Display the fetched fact
            document.getElementById('factDisplay').innerText = data.fact;
            // Ensure facts section is shown
            document.getElementById('factsPage').style.display = "block";
            // Hide topic selection if visible
            document.getElementById('topicSelection').style.display = "none";  
        })
        .catch(error => console.error('Error fetching fact:', error));
}
