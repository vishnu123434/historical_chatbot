// Function to fetch and load quiz topics
function loadQuizTopics() {
    // Hide the facts container when selecting quiz
    document.getElementById('fact-container').style.display = 'none';
  
    // Fetch quiz topics and display them
    fetch('/get_quiz_topics')
      .then(response => response.json())
      .then(topics => {
        let topicContent = "";
        topics.forEach(topic => {
          topicContent += `
            <button onclick="loadQuizQuestions('${topic.topic_name}')">${topic.topic_name}</button>
          `;
        });
  
        document.getElementById('content-area').innerHTML = topicContent;
      });
  }
  
  // Function to fetch and load quiz questions for a selected topic
  function loadQuizQuestions(topicName) {
    // Hide the fact container when selecting quiz
    document.getElementById('fact-container').style.display = 'none';
  
    // Clear previous quiz content
    document.getElementById('content-area').innerHTML = '';
  
    fetch(`/get_quiz_questions/${topicName}`)
      .then(response => response.json())
      .then(questions => {
        let quizContent = '<h3>Quiz Questions</h3><p>Answer the following questions:</p>';
  
        questions.forEach((question, index) => {
          quizContent += `
            <div class="quiz-container">
              <div class="quiz-question" id="quiz-question-${index}">
                <p><strong>${index + 1}. ${question.question_text}</strong></p>
                <div class="quiz-options">
                  <label class="quiz-option">
                    <input type="radio" name="question-${index}" value="A"> A) ${question.option_a}
                  </label>
                  <label class="quiz-option">
                    <input type="radio" name="question-${index}" value="B"> B) ${question.option_b}
                  </label>
                  <label class="quiz-option">
                    <input type="radio" name="question-${index}" value="C"> C) ${question.option_c}
                  </label>
                  <label class="quiz-option">
                    <input type="radio" name="question-${index}" value="D"> D) ${question.option_d}
                  </label>
                </div>
                <button onclick="checkAnswer(${index}, '${question.correct_answer}')">Submit Answer</button>
                <p id="answer-${index}"></p>
              </div>
            </div>
          `;
        });
  
        document.getElementById('content-area').innerHTML = quizContent;
      });
  }
  
  // Function to check if the selected answer is correct
  function checkAnswer(questionIndex, correctAnswer) {
    const selectedOption = document.querySelector(`input[name="question-${questionIndex}"]:checked`);
    const answerElement = document.getElementById(`answer-${questionIndex}`);
  
    if (selectedOption) {
      if (selectedOption.value === correctAnswer) {
        answerElement.textContent = "Correct!";
        answerElement.className = 'correct';
      } else {
        answerElement.textContent = `Incorrect! The correct answer was ${correctAnswer}.`;
        answerElement.className = 'incorrect';
      }
    } else {
      answerElement.textContent = "Please select an answer.";
      answerElement.style.color = "orange";
    }
  }
  
 