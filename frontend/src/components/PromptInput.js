import React, { useState } from 'react';
import '../styles/PromptInput.css';

function PromptInput({ onAnalyze, loading }) {
  const [prompt, setPrompt] = useState('');
  const [domain, setDomain] = useState('general');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onAnalyze(prompt, domain);
    }
  };

  return (
    <div className="prompt-input-container">
      <form onSubmit={handleSubmit}>
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

        <div className="input-group">
          <label htmlFor="domain">Domain:</label>
          <select
            id="domain"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            disabled={loading}
          >
            <option value="general">General</option>
            <option value="political">Political</option>
            <option value="science">Science</option>
            <option value="medical">Medical</option>
          </select>
        </div>

        <button type="submit" disabled={loading || !prompt.trim()}>
          {loading ? 'Analyzing...' : 'Analyze Prompt'}
        </button>
      </form>
    </div>
  );
}

export default PromptInput;
