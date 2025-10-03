import React, { useState } from 'react';
import '../styles/ResultDisplay.css';

function ResultDisplay({ originalPrompt, rewrittenPrompt, changesMade, alternatives }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="result-display">
      <h2>Objective Rewrite</h2>

      <div className="comparison">
        <div className="original">
          <h3>Original Prompt</h3>
          <div className="prompt-box">
            <p>{originalPrompt}</p>
          </div>
        </div>

        <div className="arrow">→</div>

        <div className="rewritten">
          <h3>Rewritten Prompt</h3>
          <div className="prompt-box">
            <p>{rewrittenPrompt}</p>
            <button
              className="copy-button"
              onClick={() => handleCopy(rewrittenPrompt)}
            >
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
        </div>
      </div>

      {changesMade.length > 0 && (
        <div className="changes-made">
          <h3>Changes Applied:</h3>
          <ul>
            {changesMade.map((change, idx) => (
              <li key={idx}>{change}</li>
            ))}
          </ul>
        </div>
      )}

      {alternatives.length > 0 && (
        <div className="alternatives">
          <h3>Alternative Suggestions:</h3>
          <ul>
            {alternatives.map((alt, idx) => (
              <li key={idx}>
                <span>{alt}</span>
                <button
                  className="copy-button-small"
                  onClick={() => handleCopy(alt)}
                >
                  Copy
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ResultDisplay;
