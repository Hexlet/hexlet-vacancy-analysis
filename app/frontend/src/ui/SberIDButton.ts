import React, { MouseEventHandler } from 'react';

interface SberIDButtonProps {
  onClick: MouseEventHandler<HTMLButtonElement>;
  size?: number;
}

export const SberIDButton = ({ onClick, size = 24 }: SberIDButtonProps) => {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: '#4CAF50',
        border: 'none',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        cursor: 'pointer',
      }}
    >
      <svg
        role="img"
        viewBox="0 0 24 24"
        fill="none"
        stroke="#fff"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        style={{
          width: size * 0.6,
          height: size * 0.6,
        }}
      >
        <polyline points="20 6 9 17 4 12" />
      </svg>
    </button>
  );
};

export default SberIDButton;