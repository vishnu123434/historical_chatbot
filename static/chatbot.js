document.getElementById("send-btn").addEventListener("click", function() {
    let userInput = document.getElementById("user-input").value;
    if (userInput) {
        // Add user's message to the chat display
        addMessageToChat('user', userInput);
        document.getElementById("user-input").value = "";  // Clear the input field

        // Simulate bot's reply with its name, icon, and message
        setTimeout(function() {
            let botReply = getBotReply(userInput);  // Function for bot response
            addMessageToChat('bot', botReply);
        }, 1000);  // Simulate slight delay
    }
});

// Function to add message to chat
function addMessageToChat(sender, message) {
    const chatDisplay = document.getElementById("chat-display");
    const messageElement = document.createElement("div");

    // Format message based on sender
    if (sender === 'user') {
        messageElement.innerHTML = `<div class="user-message"><strong>You:</strong> ${message}</div>`;
    } else {
        messageElement.innerHTML = `
            <div class="bot-message">
                <img src="${botIconUrl}" class="bot-icon" alt="Bot Icon" />
                <strong>Vyasa:</strong> ${message}
            </div>
        `;
    }

    chatDisplay.appendChild(messageElement);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;  // Auto scroll to the bottom
}

// Function to simulate bot's response based on user input
function getBotReply(input) {
    // Customize the bot's response based on user input
    if (input.toLowerCase().includes("hello")) {
        return "Hello! How can I assist you today?";
    } else {
        return "Sorry, I didn't quite understand that. Could you ask something else?";
    }
}