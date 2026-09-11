import React from 'react';

interface LevelOption {
  value: string;
  label: string;
  description: string;
}

const LEVELS: LevelOption[] = [
  {
    value: 'beginner',
    label: 'Beginner',
    description: 'Simple language with analogies — no prior knowledge needed',
  },
  {
    value: 'intermediate',
    label: 'Intermediate',
    description: 'Moderate detail with domain terms briefly explained',
  },
  {
    value: 'advanced',
    label: 'Advanced',
    description: 'Technical depth with precise terminology',
  },
];

interface LevelSelectorProps {
  level: string;
  onChange: (level: string) => void;
}

const LevelSelector: React.FC<LevelSelectorProps> = ({ level, onChange }) => {
  return (
    <div className="level-selector" role="group" aria-label="Difficulty level">
      {LEVELS.map((option) => {
        const isActive = level === option.value;
        return (
          <div key={option.value} className="level-selector__option">
            <button
              type="button"
              className={`level-selector__btn${isActive ? ' level-selector__btn--active' : ''}`}
              onClick={() => onChange(option.value)}
              aria-pressed={isActive}
            >
              {option.label}
            </button>
            <p className="level-selector__description">{option.description}</p>
          </div>
        );
      })}
    </div>
  );
};

export default LevelSelector;
