// Common function to handle sending a message
async function handleUserInput() {
    const userInputField = document.getElementById("user-input");
    const userInput = userInputField.value.trim();

    if (userInput) {
        // Clear the input field immediately
        userInputField.value = "";

        // Add the user's message to the chat display
        addMessageToChat('user', userInput);

        try {
            // Fetch the bot's reply from the backend
            const botReply = await getBotReply(userInput);
            addMessageToChat('bot', botReply);
        } catch (error) {
            addMessageToChat('bot', "Sorry, I couldn't process your request.");
            console.error("Error fetching bot reply:", error);
        }
    }
}

// Function to add messages to the chat display
function addMessageToChat(sender, message) {
    const chatDisplay = document.getElementById("chat-display");
    const messageElement = document.createElement("div");

    if (sender === 'user') {
        // User's message layout
        messageElement.classList.add("message", "user-message");
        messageElement.innerHTML = `<strong>You:</strong> ${message}`;
    } else if (sender === 'bot') {
        // Bot's message layout
        messageElement.classList.add("message", "bot-message");
        messageElement.innerHTML = `
            <strong>Vyasa:</strong> 
            <span class="bot-reply">${message}</span>
        `;
    }

    // Append the message and auto-scroll
    chatDisplay.appendChild(messageElement);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

// Function to fetch the bot's response from the backend
async function getBotReply(input) {
    const response = await fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
    });

    if (response.ok) {
        const data = await response.json();
        return data.results?.[0]?.chunk || "I couldn't find any information related to your query.";
    } else {
        throw new Error("Failed to fetch response from the backend.");
    }
}

// Event listener for the "Send" button
document.getElementById("send-btn").addEventListener("click", async function () {
    await handleUserInput();
});

// Event listener for "Enter" or "Space" key press
document.getElementById("user-input").addEventListener("keydown", async function (event) {
    if (event.key === 'Enter' || event.key === ' ') {  // 'Enter' or 'Space' key
        event.preventDefault(); // Prevent default behavior (such as form submission)
        await handleUserInput();
    }
});
