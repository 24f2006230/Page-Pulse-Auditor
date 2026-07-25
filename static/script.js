document.getElementById('auditForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const urlInput = document.getElementById('urlInput').value;
    const submitBtn = document.getElementById('submitBtn');
    const resultsArea = document.getElementById('resultsArea');

    submitBtn.innerText = 'Auditing...';
    submitBtn.disabled = true;
    resultsArea.style.display = 'block';
    resultsArea.innerHTML = '<div class="alert alert-info">Fetching data...</div>';

    try {
        const response = await fetch('http://127.0.0.1:5000/api/audit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: urlInput })
        });
        const data = await response.json();
        if (!response.ok || data.error) {
            resultsArea.innerHTML = `<div class="alert alert-danger">Error: ${data.error || 'Something went wrong.'}</div>`;
            return;
        }
        resultsArea.innerHTML = `
            <div class="card shadow-sm p-4">
                <h5>Audit Results</h5>
                <pre class="bg-dark text-light p-3 rounded"><code>${JSON.stringify(data, null, 2)}</code></pre>
            </div>
        `;

    } catch (error) {
        resultsArea.innerHTML = `<div class="alert alert-danger">Failed to connect to the server.</div>`;
    } finally {
        submitBtn.innerText = 'Run Audit';
        submitBtn.disabled = false;
    }
});