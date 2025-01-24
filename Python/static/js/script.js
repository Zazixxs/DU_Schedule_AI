async function sendPrompt() {
    const prompt = document.getElementById('prompt').value;
    const responseDiv = document.getElementById('response');
    const promptField = document.getElementById('prompt');
    responseDiv.textContent = "Loading...";
    try {
        const response = await fetch('/ask_ollama', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const result = await response.json();
        if (response.ok) {
            responseDiv.textContent = result.response || "No response";
        } else {
            responseDiv.textContent = `Error: ${result.error || "Unknown error"}`;
        }
    } catch (error) {
        responseDiv.textContent = "Error connecting to the server.";
    } finally {
        promptField.value = "";
    }
}

async function fetchRecommendations() {
    const recommendationsContainer = document.getElementById('recommendations');
    recommendationsContainer.textContent = "Loading AI recommendations...";
    try {
        const response = await fetch('/get_recommendations', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            const data = await response.json();
            // Display the response (assumes it's a single string)
            recommendationsContainer.innerHTML = `<p>${data}</p>`;
        } else {
            recommendationsContainer.textContent = `Error: ${response.statusText || "Unable to fetch recommendations"}`;
        }
    } catch (error) {
        recommendationsContainer.textContent = "Error connecting to the server.";
        console.error("Fetch Recommendations Error:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    fetchRecommendations();
});


