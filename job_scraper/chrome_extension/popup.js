// API endpoint - update this with your server URL
const API_URL = 'http://localhost:8000/job-collection/page';
const API_HEALTH_URL = 'http://localhost:8000/'

// DOM elements
const form = document.getElementById('saveForm');
const urlInput = document.getElementById('urlInput');
const submitBtn = document.getElementById('submitBtn');
const statusDiv = document.getElementById('status');
const connectionStatus = document.getElementById('api_connection_status')

// Get the current tab's URL and HTML
async function getCurrentTabInfo() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Get the page HTML
  const [{ result: html }] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => document.documentElement.outerHTML
  });

  return {
    url: tab.url,
    html: html
  };
}

// Show status message
function showStatus(message, isError = false) {
  statusDiv.textContent = message;
  statusDiv.className = isError ? 'status error' : 'status success';
  statusDiv.classList.remove('hidden');

  // Hide status after 5 seconds
  setTimeout(() => {
    statusDiv.classList.add('hidden');
  }, 5000);
}

// Save job page to the database
async function saveJobPage(url, pageHtml) {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        page_html: pageHtml
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to save job page');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
}

// Handle form submission
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Disable submit button
  submitBtn.disabled = true;
  submitBtn.textContent = 'Saving...';

  try {
    // Get current tab info
    const tabInfo = await getCurrentTabInfo();

    // Use custom URL if provided, otherwise use current tab URL
    const targetUrl = urlInput.value.trim() || tabInfo.url;
    let pageHtml = tabInfo.html;

    // If a custom URL is provided, fetch its HTML
    if (urlInput.value.trim()) {
      showStatus('Fetching page content...', false);
      const fetchResponse = await fetch(targetUrl);
      if (!fetchResponse.ok) {
        throw new Error('Failed to fetch the specified URL');
      }
      pageHtml = await fetchResponse.text();
    }

    // Save to database
    const result = await saveJobPage(targetUrl, pageHtml);

    // Show success message
    showStatus(`✓ Saved! Page ID: ${result.page_id}`, false);

    // Clear the input
    urlInput.value = '';

  } catch (error) {
    showStatus(error.message, true);
  } finally {
    // Re-enable submit button
    submitBtn.disabled = false;
    submitBtn.textContent = 'Save Job Page';
  }
});

// Auto-fill current URL on load (for reference)
(async () => {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    urlInput.placeholder = `Leave blank to use: ${tab.url}`;
  } catch (error) {
    console.error('Error getting current tab:', error);
  }
})();

(async () => {
  try {
    const res = await fetch(API_HEALTH_URL, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!res.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to connect to backend');
    }

    api_connection_status.textContent = "Connected"
  } catch (error) {
    api_connection_status.textContent = "Failed to connect"
  }

})();
