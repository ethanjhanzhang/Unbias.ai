import React, { useState } from 'react';
import '../styles/PromptInput.css';

function PromptInput({ onAnalyze, loading }) {
  const [prompt, setPrompt] = useState('');
  const [mode, setMode] = useState('nlp');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onAnalyze(prompt, mode);
    }
  };

  return (
    <div className="prompt-input-container">
      <form onSubmit={handleSubmit}>
        <div className="mode-selector">
          <label>Analysis Mode:</label>
          <div className="mode-buttons">
            <button
              type="button"
              className={`mode-button ${mode === 'nlp' ? 'active' : ''}`}
              onClick={() => setMode('nlp')}
              disabled={loading}
            >
              🔍 Basic Mode
              <span className="mode-desc">Rule-based pattern matching</span>
            </button>
            <button
              type="button"
              className={`mode-button ${mode === 'ai' ? 'active' : ''}`}
              onClick={() => setMode('ai')}
              disabled={loading}
            >
              🤖 AI Mode
              <span className="mode-desc">Gemini-powered analysis</span>
            </button>
          </div>
        </div>

        <div className="input-group">
          <label htmlFor="prompt">Enter your prompt:</label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your question or prompt here..."
            rows="5"
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading || !prompt.trim()}>
          {loading ? 'Analyzing...' : 'Analyze Prompt'}
        </button>
      </form>
    </div>
  );
}

export default PromptInput;
