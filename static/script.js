document.getElementById("sendBtn").addEventListener("click", async () => {
    const input = document.getElementById("userInput").value.trim();
    if (!input) return alert("Please enter your prompt!");

    const responseCard = document.getElementById("responseCard");
    const responseText = document.getElementById("responseText");

    responseText.innerHTML = "";
    responseCard.classList.remove("hidden");

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
        typingIndicator.remove();

        responseText.innerText = data.response || ("Error: " + data.error);
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

// Auto-upload when file selected
document.getElementById("fileInput").addEventListener("change", async () => {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) return;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const responseCard = document.getElementById("responseCard");
    const responseText = document.getElementById("responseText");
    responseText.innerHTML = "";
    responseCard.classList.remove("hidden");

    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("typing-indicator");
    typingIndicator.innerHTML = "<span></span><span></span><span></span>";
    responseText.appendChild(typingIndicator);

    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        typingIndicator.remove();
        responseText.innerText = data.response || ("Error: " + data.error);

    } catch (err) {
        typingIndicator.remove();
        responseText.innerText = "Error: " + err.message;
    }
});
