$(document).ready(function() {
    // Event listener for "Give a Fact" button
    $('#giveFactBtn').click(function() {
        $.ajax({
            url: '/give_fact',
            method: 'GET',
            success: function(data) {
                $('#factArea').text(data.fact);
            }
        });
    });

    // Event listener for "Take a Quiz" button
    $('#takeQuizBtn').click(function() {
        $.ajax({
            url: '/take_quiz',
            method: 'GET',
            success: function(data) {
                $('#quizArea').html(`
                    <p>${data.question}</p>
                    <ul>
                        <li><input type="radio" name="quizOption" value="${data.option_a}"> ${data.option_a}</li>
                        <li><input type="radio" name="quizOption" value="${data.option_b}"> ${data.option_b}</li>
                        <li><input type="radio" name="quizOption" value="${data.option_c}"> ${data.option_c}</li>
                        <li><input type="radio" name="quizOption" value="${data.option_d}"> ${data.option_d}</li>
                    </ul>
                    <button id="submitQuiz">Submit Answer</button>
                `);

                // Handle quiz submission
                $('#submitQuiz').click(function() {
                    let selectedOption = $('input[name="quizOption"]:checked').val();

                    if (!selectedOption) {
                        alert('Please select an option!');
                        return;
                    }

                    if (selectedOption === data.correct_answer) {
                        // Correct answer: highlight in green
                        $('input[name="quizOption"]:checked').parent().css('color', 'green');
                    } else {
                        // Wrong answer: highlight in red and show the correct answer
                        $('input[name="quizOption"]:checked').parent().css('color', 'red');
                        $('input[name="quizOption"][value="' + data.correct_answer + '"]').parent().css('color', 'green');
                    }
                });
            }
        });
    });

    // Event listener for chatbot interaction
    $('#sendBtn').click(function() {
        let userMessage = $('#userInput').val();
        $.ajax({
            url: '/chatbot',
            method: 'POST',
            data: { message: userMessage },
            success: function(data) {
                $('#chatbotResponse').text(data.fact);
            }
        });
    });
});
