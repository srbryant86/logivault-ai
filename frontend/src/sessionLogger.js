// src/services/sessionLogger.js

export async function logSession({ prompt, result, retries, error }) {
  const payload = {
    prompt,
    result,
    retries,
    error: error?.message || null,
    timestamp: new Date().toISOString(),
    client: 'logivault-editor',
  };

  try {
    await fetch(`${process.env.REACT_APP_API_URL}/log-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    console.warn('[Session Logger] Failed:', e.message);
  }
}