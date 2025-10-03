import React from 'react';
import '../styles/BiasDisplay.css';

function BiasDisplay({ biasScore, biases, originalPrompt, domain, domainConfidence }) {
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

  const getDomainEmoji = (domain) => {
    const emojiMap = {
      'political': '🏛️',
      'science': '🔬',
      'medical': '⚕️',
      'general': '💬'
    };
    return emojiMap[domain] || '💬';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence === 'high') return '#4caf50';
    if (confidence === 'medium') return '#ff9800';
    return '#f44336';
  };

  const highlightBiases = () => {
    const allBiases = [];

    Object.entries(biases).forEach(([type, items]) => {
      items.forEach(item => {
        allBiases.push({ ...item, type });
      });
    });

    if (allBiases.length === 0) {
      return originalPrompt;
    }

    // Sort by position (ascending order)
    allBiases.sort((a, b) => a.position - b.position);

    // Remove overlapping biases (keep first occurrence)
    const nonOverlapping = [];
    allBiases.forEach(bias => {
      const overlaps = nonOverlapping.some(existing =>
        (bias.position >= existing.position && bias.position < existing.position + existing.length) ||
        (existing.position >= bias.position && existing.position < bias.position + bias.length)
      );
      if (!overlaps) {
        nonOverlapping.push(bias);
      }
    });

    // Build highlighted text using React elements approach instead of dangerouslySetInnerHTML
    const parts = [];
    let lastIndex = 0;

    nonOverlapping.forEach((bias, idx) => {
      // Add text before bias
      if (bias.position > lastIndex) {
        parts.push(originalPrompt.substring(lastIndex, bias.position));
      }

      // Add highlighted bias text
      const biasText = originalPrompt.substring(bias.position, bias.position + bias.length);
      parts.push(
        <mark
          key={idx}
          className="bias-highlight"
          title={bias.type.replace(/_/g, ' ')}
        >
          {biasText}
        </mark>
      );

      lastIndex = bias.position + bias.length;
    });

    // Add remaining text
    if (lastIndex < originalPrompt.length) {
      parts.push(originalPrompt.substring(lastIndex));
    }

    return parts;
  };

  const totalBiases = Object.values(biases).reduce((sum, arr) => sum + arr.length, 0);

  return (
    <div className="bias-display">
      <h2>Bias Analysis</h2>

      <div className="domain-detected">
        <span className="domain-emoji">{getDomainEmoji(domain)}</span>
        <span className="domain-label">
          Detected Domain: <strong style={{ textTransform: 'capitalize' }}>{domain}</strong>
        </span>
        <span
          className="domain-confidence"
          style={{ color: getConfidenceColor(domainConfidence) }}
        >
          ({domainConfidence} confidence)
        </span>
      </div>

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
            <div className="prompt-highlight">
              {highlightBiases()}
            </div>
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
