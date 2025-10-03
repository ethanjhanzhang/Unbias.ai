import React from 'react';
import '../styles/BiasDisplay.css';

function BiasDisplay({ biasScore, biases, originalPrompt }) {
  const getScoreColor = (score) => {
    if (score < 30) return '#4caf50';
    if (score < 60) return '#ff9800';
    return '#f44336';
  };

  const getScoreLabel = (score) => {
    if (score < 30) return 'Low Bias';
    if (score < 60) return 'Moderate Bias';
    return 'High Bias';
  };

  const highlightBiases = () => {
    let highlighted = originalPrompt;
    const allBiases = [];

    Object.entries(biases).forEach(([type, items]) => {
      items.forEach(item => {
        allBiases.push({ ...item, type });
      });
    });

    // Sort by position (reverse order to maintain string indices)
    allBiases.sort((a, b) => b.position - a.position);

    allBiases.forEach(bias => {
      const before = highlighted.substring(0, bias.position);
      const biasText = highlighted.substring(bias.position, bias.position + bias.length);
      const after = highlighted.substring(bias.position + bias.length);
      highlighted = `${before}<mark class="bias-highlight" title="${bias.type}">${biasText}</mark>${after}`;
    });

    return { __html: highlighted };
  };

  const totalBiases = Object.values(biases).reduce((sum, arr) => sum + arr.length, 0);

  return (
    <div className="bias-display">
      <h2>Bias Analysis</h2>

      <div className="bias-score-container">
        <div className="bias-score" style={{ color: getScoreColor(biasScore) }}>
          <span className="score-number">{biasScore}</span>
          <span className="score-label">{getScoreLabel(biasScore)}</span>
        </div>
        <div className="bias-count">
          {totalBiases} bias indicator{totalBiases !== 1 ? 's' : ''} detected
        </div>
      </div>

      {totalBiases > 0 && (
        <>
          <div className="highlighted-text">
            <h3>Highlighted Biases:</h3>
            <div
              className="prompt-highlight"
              dangerouslySetInnerHTML={highlightBiases()}
            />
          </div>

          <div className="bias-breakdown">
            <h3>Bias Breakdown:</h3>
            <ul>
              {Object.entries(biases).map(([type, items]) => (
                items.length > 0 && (
                  <li key={type}>
                    <strong>{type.replace(/_/g, ' ').toUpperCase()}:</strong> {items.length}
                    <ul className="bias-items">
                      {items.map((item, idx) => (
                        <li key={idx}>{item.term}</li>
                      ))}
                    </ul>
                  </li>
                )
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}

export default BiasDisplay;
