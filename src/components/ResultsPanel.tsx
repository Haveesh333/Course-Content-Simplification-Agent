import React from 'react';

interface ResultsPanelProps {
  explanation: string;
  keyPoints: string[];
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({ explanation, keyPoints }) => {
  return (
    <section className="results-panel">
      <h2 className="results-panel__title">Simplified Explanation</h2>
      <p className="results-panel__explanation">{explanation}</p>

      {keyPoints.length > 0 && (
        <>
          <h3 className="results-panel__subtitle">Key Points</h3>
          <ul className="results-panel__key-points">
            {keyPoints.map((point, index) => (
              <li key={index} className="results-panel__key-point">
                {point}
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
};

export default ResultsPanel;
