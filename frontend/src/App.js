import React, { useState } from 'react';
import PromptInput from './components/PromptInput';
import BiasDisplay from './components/BiasDisplay';
import ResultDisplay from './components/ResultDisplay';
import { analyzePrompt } from './services/api';
import './styles/App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (prompt, mode) => {
    setLoading(true);
    setError(null);

    try {
      const data = await analyzePrompt(prompt, mode);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze prompt. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Prompt Objectivity Analyzer</h1>
        <p className="subtitle">Transform biased prompts into objective inquiries</p>
      </header>

      <main className="App-main">
        <PromptInput onAnalyze={handleAnalyze} loading={loading} />

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {result && (
          <>
            <BiasDisplay
              biasScore={result.bias_score}
              biases={result.biases_detected}
              originalPrompt={result.original_prompt}
              domain={result.domain}
              domainConfidence={result.domain_confidence}
            />

            <ResultDisplay
              originalPrompt={result.original_prompt}
              rewrittenPrompt={result.rewritten_prompt}
              changesMade={result.changes_made}
              alternatives={result.alternative_suggestions}
            />
          </>
        )}
      </main>

      <footer className="App-footer">
        <p>Built to combat echo chambers and promote objective AI interactions</p>
      </footer>
    </div>
  );
}

export default App;
