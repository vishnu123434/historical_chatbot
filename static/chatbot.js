document.getElementById("send-btn").addEventListener("click", function() {
    let userInput = document.getElementById("user-input").value;
    if (userInput) {
        // Add user's message to the chat display
        addMessageToChat('user', userInput);
        document.getElementById("user-input").value = "";  // Clear the input field

        // Simulate bot's reply with its name and icon
        setTimeout(function() {
            let botReply = getBotReply(userInput);  // You can implement a function for more complex responses
            addMessageToChat('bot', botReply);
        }, 1000);  // Simulating a slight delay in bot's reply
    }
});

// Function to add message to chat
function addMessageToChat(sender, message) {
    const chatDisplay = document.getElementById("chat-display");
    const messageElement = document.createElement("div");

    // Format message based on sender (user or bot)
    if (sender === 'user') {
        messageElement.innerHTML = `<div class="user-message"><strong>You:</strong> ${message}</div>`;
    } else {
        messageElement.innerHTML = `
            <div class="bot-message">
                <img src="/static/chatbot-icon.png" alt="Chatbot Icon" class="bot-icon">
                <strong>ChatBot:</strong> ${message}
            </div>
        `;
    }

    chatDisplay.appendChild(messageElement);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;  // Auto scroll to the bottom
}

// Function to simulate bot's response based on user input
function getBotReply(input) {
    // Customize the bot's response based on user input
    // This is a simple placeholder; you can replace it with your own logic
    if (input.toLowerCase().includes("hello")) {
        return "Hello! How can I assist you today?";
    } else {
        return "Sorry, I didn't quite understand that. Could you ask something else?";
    }
}
