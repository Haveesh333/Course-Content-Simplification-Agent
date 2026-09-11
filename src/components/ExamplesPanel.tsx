import React from 'react';

interface ExamplesPanelProps {
  examples: string[];
}

const ExamplesPanel: React.FC<ExamplesPanelProps> = ({ examples }) => {
  if (examples.length === 0) return null;

  return (
    <section className="examples-panel">
      <h2 className="examples-panel__title">Examples</h2>
      <ol className="examples-panel__list">
        {examples.map((example, index) => (
          <li key={index} className="examples-panel__item">
            {example}
          </li>
        ))}
      </ol>
    </section>
  );
};

export default ExamplesPanel;
