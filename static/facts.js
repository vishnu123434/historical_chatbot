// Function to fetch and display a random fact
function loadRandomFact() {
    // Hide the quiz container when switching to facts
    document.getElementById('content-area').innerHTML = '';
    
    // Show the fact container when the 'Random Facts' button is clicked
    document.getElementById('fact-container').style.display = 'block';

    fetch('/api/random_fact')
        .then(response => response.json())
        .then(data => {
            // Display the fetched fact
            document.getElementById('fact-container').innerText = data.fact;
        })
        .catch(error => console.error('Error fetching fact:', error));
}
