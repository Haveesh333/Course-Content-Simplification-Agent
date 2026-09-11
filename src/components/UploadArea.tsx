import React, { useRef, useState } from 'react';

interface UploadAreaProps {
  file: File | null;
  onFileChange: (file: File | null) => void;
}

const UploadArea: React.FC<UploadAreaProps> = ({ file, onFileChange }) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] ?? null;
    onFileChange(selected);
    // Reset input so same file can be re-selected after removal
    e.target.value = '';
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0] ?? null;
    onFileChange(dropped);
  };

  const handleRemove = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    onFileChange(null);
  };

  return (
    <div
      className={`upload-area${dragging ? ' upload-area--dragging' : ''}${file ? ' upload-area--has-file' : ''}`}
      onClick={handleClick}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && handleClick()}
      aria-label="File upload area"
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt"
        className="upload-area__input"
        onChange={handleInputChange}
      />
      {file ? (
        <div className="upload-area__file-info">
          <span className="upload-area__filename">{file.name}</span>
          <button
            type="button"
            className="upload-area__remove-btn"
            onClick={handleRemove}
            aria-label="Remove file"
          >
            Remove
          </button>
        </div>
      ) : (
        <span className="upload-area__prompt">
          Drag &amp; drop a PDF or TXT file here, or click to browse
        </span>
      )}
    </div>
  );
};

export default UploadArea;
