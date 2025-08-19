document.getElementById("sendBtn").addEventListener("click", async () => {
    const input = document.getElementById("userInput").value.trim();
    if (!input) return alert("Please enter your prompt!");

    const responseCard = document.getElementById("responseCard");
    const responseText = document.getElementById("responseText");

    // Clear previous response and show the card
    responseText.innerHTML = "";
    responseCard.classList.remove("hidden");

    // Show AI typing animation
    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("typing-indicator");
    typingIndicator.innerHTML = "<span></span><span></span><span></span>";
    responseText.appendChild(typingIndicator);

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({input: input})
        });

        const data = await res.json();

        // Remove typing animation
        typingIndicator.remove();

        if (data.response) {
            responseText.innerText = data.response; // Show AI response
        } else {
            responseText.innerText = "Error: " + data.error;
        }
    } catch (err) {
        typingIndicator.remove();
        responseText.innerText = "Error: " + err.message;
    }
});

async function sendFeedback(feedback) {
    try {
        await fetch("/feedback", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({feedback})
        });
        alert("Feedback recorded!");
    } catch (err) {
        alert("Failed to record feedback: " + err.message);
    }
}