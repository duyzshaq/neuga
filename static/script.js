document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const welcomeMessage = document.getElementById('welcome-message');
    const typingIndicator = document.getElementById('typing-indicator');
    const sendBtn = document.getElementById('send-btn');

    let isProcessing = false;

    // Auto-focus input on load
    userInput.focus();

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();

        if (message && !isProcessing) {
            handleUserMessage(message);
        }
    });

    async function handleUserMessage(message) {
        // Disable input while processing
        isProcessing = true;
        userInput.disabled = true;
        sendBtn.disabled = true;

        // Remove welcome message if it exists
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }

        // Add user message to UI
        addMessage(message, 'user');
        userInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        try {
            // Call API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Hide typing indicator
            hideTypingIndicator();

            if (response.ok) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Sorry, something went wrong. Please try again.', 'bot');
                console.error('Error:', data.error);
            }

        } catch (error) {
            hideTypingIndicator();
            addMessage('Network error. Please check your connection.', 'bot');
            console.error('Network Error:', error);
        } finally {
            // Re-enable input
            isProcessing = false;
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const avatar = document.createElement('div');
        avatar.classList.add('message-avatar');

        if (sender === 'user') {
            avatar.innerHTML = '<i class="fa-solid fa-user"></i>';
        } else {
            avatar.innerHTML = '<i class="fa-solid fa-robot"></i>';
        }

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');

        if (sender === 'bot') {
            // Render Markdown for bot messages
            messageContent.innerHTML = marked.parse(content);
        } else {
            // Safe plain text for user messages to prevent XSS
            messageContent.textContent = content;
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);

        chatHistory.appendChild(messageDiv);

        // Scroll to bottom
        scrollToBottom();
    }



    function showTypingIndicator() {
        typingIndicator.classList.remove('hidden');
        scrollToBottom();
    }

    function hideTypingIndicator() {
        typingIndicator.classList.add('hidden');
    }

    function scrollToBottom() {
        const chatArea = document.querySelector('.chat-area');
        chatArea.scrollTop = chatArea.scrollHeight;
    }
});