document.addEventListener("DOMContentLoaded", function () {
    const postcodeInput = document.getElementById("firstName");
    const resultsContainer = document.createElement("div");
    resultsContainer.classList.add("results-container");
    postcodeInput.parentNode.appendChild(resultsContainer);

    async function fetchNearestCourts(origin) {
        try {
            const response = await fetch("http://127.0.0.1:5000/postcode-check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ origin }),
                mode: "cors"  // ✅ Ensure CORS mode is enabled
            });
    
            if (!response.ok) throw new Error("Failed to fetch nearest courts");
    
            const data = await response.json();
            displayNearestCourts(data.courts);
        } catch (error) {
            console.error("Error fetching courts:", error);
        }
    }

    function displayNearestCourts(courts) {
        const resultsContainer = document.querySelector(".results-container");
    
        // If no courts are found, hide the container
        if (!courts || courts.length === 0) {
            resultsContainer.style.display = "none"; // Hides the div
            return;
        }
    
        // Otherwise, show the container and populate it
        resultsContainer.innerHTML = "";
        resultsContainer.style.display = "block"; // Show the div
    
        courts.forEach(court => {
            const courtDiv = document.createElement("div");
            courtDiv.classList.add("court-result");
            courtDiv.innerHTML = `
                <p><strong>${court.name}</strong></p>
                <p>Postcode: ${court.postcode}</p>
                <p>Distance: ${court.distance.toFixed(2)} miles</p>
            `;
            resultsContainer.appendChild(courtDiv);
        });
    }

    postcodeInput.addEventListener("input", function () {
        const postcode = postcodeInput.value.trim();
        if (postcode.length >= 3) {
            fetchNearestCourts(postcode);
        } else {
            resultsContainer.innerHTML = "";
        }
    });
});