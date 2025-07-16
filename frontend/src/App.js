import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    try {
      const res = await fetch('/claude', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      if (data.error) {
        setResponse('Error: ' + data.error);
      } else {
        setResponse(data.content?.[0]?.text || 'No response received');
      }
    } catch (error) {
      setResponse('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>LogiVault AI</h1>
        <p>AI-powered logging and analysis tool</p>
      </header>
      <main className="App-main">
        <div className="chat-container">
          <form onSubmit={handleSubmit} className="chat-form">
            <div className="input-group">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your prompt here..."
                rows="4"
                className="prompt-input"
                disabled={loading}
              />
                {loading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </form>
          {response && (
            <div className="response-container">
              <h3>Response:</h3>
              <div className="response-text">{response}</div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
