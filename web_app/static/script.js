document.getElementById("predictionForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // prevent page reload

    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    console.log("Sending data:", data);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("Received result:", result);

        const resultDiv = document.getElementById("result");
        resultDiv.style.display = "block";

        if (result.error) {
            resultDiv.innerHTML = `<p style="color:red">❌ Error: ${result.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <h3>🔮 Prediction Result</h3>
                <p><b>Prediction:</b> ${result.prediction}</p>
                <p><b>Confidence:</b> ${result.confidence}%</p>
                <p>Probability Placed: ${result.probability_placed}%</p>
                <p>Probability Not Placed: ${result.probability_not_placed}%</p>
                <p><i>Model Used: ${result.model_used}</i></p>
            `;
        }
    } catch (err) {
        console.error("Error:", err);
        alert("Something went wrong. Check console for details.");
    }
});
