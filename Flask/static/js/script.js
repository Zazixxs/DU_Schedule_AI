//Send Prompt
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


// Fetch recommendations
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
            if (data == null || data === "") {
                recommendationsContainer.textContent = "No recommendations available.";
            } else {
                recommendationsContainer.innerHTML = `<p>${data}</p>`;
            }
        } else {
            recommendationsContainer.textContent = `Error: ${response.statusText || "Unable to fetch recommendations"}`;
        }
    } catch (error) {
        recommendationsContainer.textContent = "Error connecting to the server.";
        console.error("Fetch Recommendations Error:", error);
    }
}

// Update model
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('input[name="model"]').forEach(radio => {
        radio.addEventListener('change', function() {
            let selectedModel = this.value;
            console.log("Vald modell:", selectedModel);
            document.getElementById('select-model').textContent = `Using ${selectedModel}`;
            fetch('/update-model', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: selectedModel })
            })
            .then(response => response.json())
            .then(data => console.log("Server response:", data))
            .catch(error => console.error("Error:", error));
        });
    });
});



// Defualt Loadings
document.addEventListener("DOMContentLoaded", () => {
    fetchRecommendations();
});
