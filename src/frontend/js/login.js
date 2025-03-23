const API_URL = 'url here';

document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

    console.log('Sending login request with:', { username, password });

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: data
        });

        if (!response.ok) {
            throw new Error('Response not OK');
        }

        const result = await response.json();
        console.log('Response result:', result);

        if (result.access_token) {
            const token = result.access_token;
            localStorage.setItem('access_token', token);
            // Optionally redirect or notify user of success
        } else {
            console.error('No access token in response', result);
        }
    } catch (error) {
        console.error('Error during login:', error);
        document.getElementById('message').innerHTML = `
            <div class="error-message">
                An error occurred. Please try again later.
            </div>
        `;
    }
});
