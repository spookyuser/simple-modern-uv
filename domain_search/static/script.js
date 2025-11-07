// API base URL
const API_BASE = '';

// UI Elements
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const results = document.getElementById('results');

// Helper functions
function showLoading() {
    loading.style.display = 'block';
    error.style.display = 'none';
    results.innerHTML = '';
}

function hideLoading() {
    loading.style.display = 'none';
}

function showError(message) {
    error.textContent = message;
    error.style.display = 'block';
    hideLoading();
}

function showResults(html) {
    results.innerHTML = html;
    hideLoading();
}

async function fetchAPI(endpoint) {
    try {
        const response = await fetch(API_BASE + endpoint);
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Request failed');
        }
        return await response.json();
    } catch (err) {
        throw new Error(err.message || 'Network error');
    }
}

// Search functions
async function searchSingle() {
    const domain = document.getElementById('singleDomain').value.trim();
    if (!domain) {
        showError('Please enter a domain name');
        return;
    }

    showLoading();
    try {
        const data = await fetchAPI(`/api/search/single?word=${encodeURIComponent(domain)}`);

        const statusClass = data.available ? 'available' : 'unavailable';
        const statusText = data.available ? 'Available!' : 'Already registered';

        showResults(`
            <h3>Search Result</h3>
            <div class="result-item ${statusClass}">
                <span class="domain-name">${data.domain}</span>
                <span class="status ${statusClass}">${statusText}</span>
            </div>
        `);
    } catch (err) {
        showError(err.message);
    }
}

async function searchDictionary() {
    const maxLength = document.getElementById('dictMaxLength').value;

    showLoading();
    try {
        const data = await fetchAPI(`/api/search/dictionary?max_length=${maxLength}`);

        if (data.count === 0) {
            showResults('<p>No available dictionary words found with those criteria.</p>');
            return;
        }

        const domainsHtml = data.available.map(domain =>
            `<div class="domain-name">${domain}</div>`
        ).join('');

        showResults(`
            <h3>Available Dictionary Words</h3>
            <div class="result-count">Found ${data.count} available domains</div>
            <div class="domain-list">
                ${domainsHtml}
            </div>
        `);
    } catch (err) {
        showError(err.message);
    }
}

async function searchCombination() {
    const word1 = document.getElementById('word1').value.trim();
    const word2 = document.getElementById('word2').value.trim();

    if (!word1 || !word2) {
        showError('Please enter both words');
        return;
    }

    showLoading();
    try {
        const data = await fetchAPI(
            `/api/search/combinations?word1=${encodeURIComponent(word1)}&word2=${encodeURIComponent(word2)}`
        );

        const statusClass = data.available ? 'available' : 'unavailable';
        const statusText = data.available ? 'Available!' : 'Already registered';

        showResults(`
            <h3>Combination Result</h3>
            <div class="result-item ${statusClass}">
                <span class="domain-name">${data.domain}</span>
                <span class="status ${statusClass}">${statusText}</span>
            </div>
        `);
    } catch (err) {
        showError(err.message);
    }
}

async function searchShortCombinations() {
    const maxLength = document.getElementById('shortMaxLength').value;

    showLoading();
    try {
        const data = await fetchAPI(`/api/search/short-combinations?max_word_length=${maxLength}`);

        if (data.count === 0) {
            showResults('<p>No available combinations found with those criteria.</p>');
            return;
        }

        const domainsHtml = data.available.map(domain =>
            `<div class="domain-name">${domain}</div>`
        ).join('');

        showResults(`
            <h3>Available Word Combinations</h3>
            <div class="result-count">Found ${data.count} available domains</div>
            <div class="domain-list">
                ${domainsHtml}
            </div>
        `);
    } catch (err) {
        showError(err.message);
    }
}

async function searchLetterNumber() {
    showLoading();
    try {
        const data = await fetchAPI('/api/search/letter-number?limit=100');

        if (data.count === 0) {
            showResults('<p>No available letter-number patterns found.</p>');
            return;
        }

        const domainsHtml = data.available.map(domain =>
            `<div class="domain-name">${domain}</div>`
        ).join('');

        showResults(`
            <h3>Available Letter-Number Patterns</h3>
            <div class="result-count">Found ${data.count} available domains</div>
            <div class="domain-list">
                ${domainsHtml}
            </div>
        `);
    } catch (err) {
        showError(err.message);
    }
}

// Add Enter key support for text inputs
document.getElementById('singleDomain').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchSingle();
});

document.getElementById('word1').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchCombination();
});

document.getElementById('word2').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchCombination();
});

// Check health on load
fetch('/api/health')
    .then(res => res.json())
    .then(data => {
        if (!data.database_loaded) {
            showError('Database not loaded. Please run the setup scripts to process the ICANN zone file first.');
        }
    })
    .catch(err => {
        showError('Unable to connect to the server. Please make sure the application is running.');
    });
