
// Function to fetch topics from the API and populate the dropdown
function loadQuizTopics() {
    fetch('/api/quiz_topics')
        .then(response => response.json())
        .then(data => {
            const topicSelect = document.getElementById("quizTopics");
            topicSelect.innerHTML = ''; // Clear existing options
            data.forEach(topic => {
                const option = document.createElement("option");
                option.value = topic[0]; // topic_id
                option.textContent = topic[1]; // topic_name
                topicSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching quiz topics:', error));
}

// Show topics selection dropdown and load topics
function displayTopics() {
    document.getElementById("topicSelection").style.display = "block";
    document.getElementById("factsPage").style.display = "none"; // Hide facts section if visible
    loadQuizTopics(); // Load topics into dropdown
}

let currentQuestionIndex = 0;
let quizQuestions = [];

// Function to fetch and display quiz questions after topic selection
function loadQuizQuestions(topicId) {
    fetch(`/api/quiz_questions/${topicId}`)
        .then(response => response.json())
        .then(data => {
            quizQuestions = data;
            displayQuestion();
            document.getElementById("quizQuestionsContainer").style.display = "block"; // Show quiz container
            document.getElementById("topicSelection").style.display = "none"; // Hide topic selection
        })
        .catch(error => console.error('Error fetching quiz questions:', error));
}


