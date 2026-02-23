const backendURL = "http://localhost:5000";

async function addUsage() {
    const usage = document.getElementById("usageInput").value;

    try {
        const response = await fetch(`${backendURL}/add`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ usage: parseFloat(usage) })
        });

        const data = await response.json();
        alert(data.message);
    } catch (error) {
        alert("Error connecting to backend!");
    }
}

async function analyzeUsage() {
    const recent = document.getElementById("recentInput").value;
    const recentArray = recent.split(",").map(Number);

    try {
        const response = await fetch(`${backendURL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ recent: recentArray })
        });

        const data = await response.json();

        document.getElementById("result").innerHTML = `
            <p><strong>Prediction:</strong> ${data.prediction}</p>
            <p><strong>Status:</strong> ${data.status}</p>
        `;
    } catch (error) {
        alert("Error analyzing data!");
    }
}