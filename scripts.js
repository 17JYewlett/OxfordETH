document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent page refresh

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let errorMessage = document.getElementById("errorMessage");

    // Simple validation check
    if (!email.includes("@") || password.length < 6) {
        errorMessage.textContent = "Invalid email or password (min 6 characters).";
        errorMessage.style.display = "block";
    } else {
        errorMessage.style.display = "none";
        alert("Login successful!");
        // Redirect or perform further actions here
    }
});

function toggleMenu() {
    document.querySelector(".nav-links").classList.toggle("active");
}

// Show loading screen when navigating to login
function showLoadingScreen() {
    const loadingScreen = document.getElementById("loadingScreen");
    loadingScreen.style.display = "flex";
    setTimeout(() => {
        window.location.href = "login.html";
    }, 1200); // Delay for effect
}

// Redirect from landing page
function redirectToLogin() {
    showLoadingScreen();
}

function showLoadingScreen() {
    const loadingScreen = document.getElementById("loadingScreen");
    loadingScreen.style.display = "flex";
    setTimeout(() => {
        window.location.href = "login.html";
    }, 1200);
}

function redirectToLogin() {
    showLoadingScreen();
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("createAccountForm");
    const accountFormContainer = document.getElementById("accountFormContainer");
    const successContainer = document.getElementById("successContainer");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the page from reloading

        console.log("Form submitted! Hiding form..."); // Debugging check

        // Hide the form container
        if (accountFormContainer) {
            accountFormContainer.style.display = "none";
            console.log("Form hidden successfully.");
        }

        // Show the success message
        if (successContainer) {
            successContainer.style.display = "flex";
            console.log("Success container displayed.");
        }
    });
});

function goBack(page) {
    window.location.href = page;
}

// Fetch all transactions from your Flask Backend
fetch("http://localhost:5000/get_transactions")
.then(response => response.json())
.then(data => {
    // Display transactions in your HTML
    data.transactions.forEach(txn => {
        const transactionList = document.getElementById("transaction-list");
        const li = document.createElement('li');
        li.innerHTML = `
        Player: ${txn.player}<br>
        Coach: ${txn.coach}<br>
        Amount: ${txn.amount}<br>
        Start Location: ${txn.startLocation}<br>
        End Location: ${txn.endLocation}<br?
        `;
        transactionList.appendChild(li);
    });
});




