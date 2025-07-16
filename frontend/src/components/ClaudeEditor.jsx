import { useState } from 'react';
import { submitPromptToClaude } from '../services/api';
import { cleanResponse, formatEditorial } from '../services/optimization';
import { logSession } from '../services/sessionLogger';
import ResponseViewer from './ResponseViewer';

// Helper function to validate API response
function isValidResponse(data) {
  return (
    data &&
    typeof data === 'object' &&
    ((data.content && typeof data.content === 'string') || 
     (Array.isArray(data.content) && data.content[0] && typeof data.content[0].text === 'string'))
  );
}

// Helper function to extract content from response
function extractContent(data) {
  if (typeof data.content === 'string') {
    return data.content;
  } else if (Array.isArray(data.content) && data.content[0] && typeof data.content[0].text === 'string') {
    return data.content[0].text;
  }
  return null;
}

export default function ClaudeEditor() {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const raw = await submitPromptToClaude(prompt);
      
      // Validate response structure
      if (!isValidResponse(raw)) {
        throw new Error('Invalid response format from Claude API');
      }
      
      const content = extractContent(raw);
      if (!content) {
        throw new Error('No valid content received from Claude API');
      }
      
      const clean = cleanResponse(content);
      const formatted = formatEditorial(clean);
      setResult(formatted);

      await logSession({
        prompt,
        result: clean,
        retries: 1,
        error: null,
      });
    } catch (err) {
      setError('Claude couldn’t process that prompt. Try again.');

      await logSession({
        prompt,
        result: null,
        retries: 3,
        error: err,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <form onSubmit={handleSubmit}>
        <label>
          Editorial Prompt:
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={6}
            style={{
              width: '100%',
              marginTop: '0.5rem',
              borderRadius: '6px',
              padding: '1rem',
              border: '1px solid #ccc',
              fontSize: '1rem',
            }}
            placeholder="Enter your editorial request..."
          />
        </label>
        <button
          disabled={loading || !prompt}
          style={{
            marginTop: '1rem',
            padding: '0.75rem 1.25rem',
            fontSize: '1rem',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'wait' : 'pointer',
          }}
        >
          {loading ? 'Generating...' : 'Submit to Claude'}
        </button>
      </form>

      {error && (
        <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>
      )}

      {result && (
        <div style={{ marginTop: '2rem' }}>
          <h3 style={{ fontWeight: 'normal' }}>Claude’s Response:</h3>
          <ResponseViewer html={result} />
        </div>
      )}
    </div>
  );
}