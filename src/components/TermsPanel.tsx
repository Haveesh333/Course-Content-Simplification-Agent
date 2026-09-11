import React from 'react';
import { DifficultTerm } from '../types';

interface TermsPanelProps {
  terms: DifficultTerm[];
}

const TermsPanel: React.FC<TermsPanelProps> = ({ terms }) => {
  if (terms.length === 0) return null;

  return (
    <section className="terms-panel">
      <h2 className="terms-panel__title">Difficult Terms</h2>
      <table className="terms-panel__table">
        <thead>
          <tr>
            <th className="terms-panel__th">Term</th>
            <th className="terms-panel__th">Simple Meaning</th>
          </tr>
        </thead>
        <tbody>
          {terms.map((item, index) => (
            <tr key={index} className="terms-panel__row">
              <td className="terms-panel__td terms-panel__td--term">{item.term}</td>
              <td className="terms-panel__td">{item.meaning}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};

export default TermsPanel;
