// Utility function to handle form submission
async function handleFormSubmission(url, data, successMessage, feedbackDiv) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok) {
            feedbackDiv.innerHTML = `<p style="color: green;">${successMessage}</p>`;
            // Optionally, you can redirect after a successful creation or login
            if (url === '/api/create-account') {
                setTimeout(() => { window.location.href = '/'; }, 2000); // Redirect to home after account creation
            }
        } else {
            feedbackDiv.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
        }
    } catch (error) {
        feedbackDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

// Account Creation
document.getElementById("create-account-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const username = document.getElementById("create-username").value;
    const password = document.getElementById("create-password").value;
    const feedbackDiv = document.getElementById("create-account-feedback");

    handleFormSubmission('/api/create-account', { username, password }, 'Account created successfully!', feedbackDiv);
});

// Login
document.getElementById("login-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const feedbackDiv = document.getElementById("login-feedback");

    handleFormSubmission('/api/login', { username, password }, 'Login successful!', feedbackDiv);
});

// Update Password
document.getElementById("update-password-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const username = document.getElementById("update-username").value;
    const old_password = document.getElementById("update-old-password").value;
    const new_password = document.getElementById("update-new-password").value;
    const feedbackDiv = document.getElementById("update-password-feedback");

    handleFormSubmission('/api/update-password', { username, old_password, new_password }, 'Password updated successfully!', feedbackDiv);
});
