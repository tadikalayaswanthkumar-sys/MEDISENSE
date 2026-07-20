import React from 'react';

export const Card = ({ children, className = '', glow = false }) => {
  return (
    <div className={`rounded-2xl glass-card p-6 transition-all duration-300 relative overflow-hidden bg-white border border-slate-200/90 shadow-sm ${glow ? 'ring-2 ring-teal-500/20 shadow-md shadow-teal-500/5' : ''} ${className}`}>
      {children}
    </div>
  );
};

export default Card;
