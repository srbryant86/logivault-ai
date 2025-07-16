const API_URL = process.env.REACT_APP_API_URL;

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
          Authorization: `Bearer ${process.env.REACT_APP_CLAUDE_KEY}`,
        },
        body: JSON.stringify({ prompt: promptText }),
      });

      if (!response.ok) {
        throw new Error(`Claude API Error: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      lastError = err;
      console.warn(`[Claude Retry ${attempt}/${retries}]`, err.message);
      await sleep(delay * attempt); // Exponential backoff
    }
  }

  throw lastError;
}