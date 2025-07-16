const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function submitPromptToClaude(promptText, retries = 3, delay = 1000) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: promptText }),
      });

      if (!response.ok) {
        // Try to get more detailed error information
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || response.statusText;
        
        // Provide specific error messages for common HTTP status codes
        let userMessage = `Claude API Error: ${response.status}`;
        if (response.status === 400) {
          userMessage = 'Invalid request: Please check your prompt and try again.';
        } else if (response.status === 401) {
          userMessage = 'Authentication failed: Please check API key configuration.';
        } else if (response.status === 429) {
          userMessage = 'Rate limit exceeded: Please wait before trying again.';
        } else if (response.status === 500) {
          userMessage = 'Server error: Please try again later.';
        } else if (response.status >= 500) {
          userMessage = 'Service unavailable: Please try again later.';
        }
        
        throw new Error(`${userMessage} (${errorMessage})`);
      }

      return await response.json();
    } catch (err) {
      lastError = err;
      console.warn(`[Claude Retry ${attempt}/${retries}]`, err.message);
      
      // Don't retry on client errors (4xx)
      if (err.message.includes('400') || err.message.includes('401')) {
        break;
      }
      
      await sleep(delay * attempt); // Exponential backoff
    }
  }

  throw lastError;
}