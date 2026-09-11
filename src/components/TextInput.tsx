import React from 'react';

interface TextInputProps {
  value: string;
  onChange: (value: string) => void;
}

const TextInput: React.FC<TextInputProps> = ({ value, onChange }) => {
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e.target.value);
  };

  const formattedCount = value.length.toLocaleString();

  return (
    <div className="text-input">
      <textarea
        className="text-input__textarea"
        value={value}
        onChange={handleChange}
        placeholder="Or paste your course content here..."
        rows={8}
        aria-label="Course content text input"
      />
      <span className="text-input__char-count">
        {formattedCount} {value.length === 1 ? 'character' : 'characters'}
      </span>
    </div>
  );
};

export default TextInput;
