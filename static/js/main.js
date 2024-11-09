// Assuming this is added in <script> tags in `login_signup.html`

function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    fetch('/login_signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: 'login',
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/main';
        } else {
            alert(data.error || "Login failed");
        }
    });
}

function signUp() {
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    fetch('/login_signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: 'signup',
            name: name,
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/main';
        } else {
            alert(data.error || "Sign-Up failed");
        }
    });
}
function searchRecords(event) {
    event.preventDefault();
    
    // Construct the natural language query based on form inputs
    const symptoms = document.getElementById("symptoms").value;
    const diagnosis = document.getElementById("diagnosis").value;
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const labResults = Array.from(
        document.querySelectorAll("#lab_results input:checked")
    ).map(cb => cb.value);

    // Create a natural language query
    let query = 'Find patients with symptoms: ${symptoms}';
    if (diagnosis) query += ', diagnosis: ${diagnosis}';
    if (age) query += ', age range: ${age}';
    if (gender) query += ', gender: ${gender}';
    if (labResults.length > 0) query += ', lab results: ${labResults.join(", ")}';

    // Send the query to the backend
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(results => {
        displayResults(results);
    })
    .catch(error => {
        console.error('Error:', error);
        const queriesDiv = document.getElementById("queries");
        queriesDiv.innerHTML = '<p style="color: red;">An error occurred. Please try again.</p>';
    });
}

