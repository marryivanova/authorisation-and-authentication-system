document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

    try {
        const response = await fetch('http://127.0.0.1:8000/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: data
        });

        const result = await response.json();

        if (response.ok) {
            const token = result.access_token;
            localStorage.setItem('access_token', token);
        } else {
            document.getElementById('message').innerHTML = `
                <div class="error-message">
                    ${result.detail || 'Invalid credentials. Please try again.'}
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('message').innerHTML = `
            <div class="error-message">
                An error occurred. Please try again later.
            </div>
        `;
        console.error('Error during login:', error);
    }
});