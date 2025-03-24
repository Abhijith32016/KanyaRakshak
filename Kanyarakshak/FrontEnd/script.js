
const API_URL = "https://your-colab-ngrok-url.com";  // Replace with your Colab API

// Send user message to chatbot backend
async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    appendMessage("You", userInput);
    document.getElementById("user-input").value = "";

    let response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        body: JSON.stringify({ text: userInput }),
        headers: { "Content-Type": "application/json" }
    });

    let result = await response.json();
    appendMessage("Bot", result.reply);
}

// Append messages to chatbox
function appendMessage(sender, message) {
    let chatBox = document.getElementById("chat-box");
    let newMessage = `<p><strong>${sender}:</strong> ${message}</p>`;
    chatBox.innerHTML += newMessage;
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Start voice input
async function startVoice() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";

    recognition.onresult = async (event) => {
        let text = event.results[0][0].transcript;
        appendMessage("You (Voice)", text);

        let response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            body: JSON.stringify({ text: text }),
            headers: { "Content-Type": "application/json" }
        });

        let result = await response.json();
        appendMessage("Bot", result.reply);
    };

    recognition.start();
}

// Send SOS alert
async function sendSOS() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            let lat = position.coords.latitude;
            let lon = position.coords.longitude;
            
            let sosMessage = `🚨 Emergency Alert! Help Needed! 📍 Location: https://maps.google.com/?q=${lat},${lon}`;
            appendMessage("System", sosMessage);

            await fetch(`${API_URL}/sos`, {
                method: "POST",
                body: JSON.stringify({ latitude: lat, longitude: lon }),
                headers: { "Content-Type": "application/json" }
            });

            alert("🚨 SOS alert sent!");
        }, () => {
            alert("Error getting location. Please allow location access.");
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}