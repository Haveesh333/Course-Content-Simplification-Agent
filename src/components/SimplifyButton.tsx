import React from 'react';

interface SimplifyButtonProps {
  onClick: () => void;
  loading: boolean;
  disabled: boolean;
}

const SimplifyButton: React.FC<SimplifyButtonProps> = ({ onClick, loading, disabled }) => {
  return (
    <button
      type="button"
      className={`simplify-btn${loading ? ' simplify-btn--loading' : ''}`}
      onClick={onClick}
      disabled={disabled || loading}
      aria-busy={loading}
    >
      {loading ? (
        <>
          <span className="simplify-btn__spinner" aria-hidden="true" />
          Processing...
        </>
      ) : (
        'Simplify'
      )}
    </button>
  );
};

export default SimplifyButton;
