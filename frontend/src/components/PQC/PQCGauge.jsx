import React, { useState, useEffect } from 'react';

export default function PQCGauge({ score, confidence }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    let current = 0;
    const interval = setInterval(() => {
      if (current >= score) {
        clearInterval(interval);
      } else {
        current += Math.ceil((score - current) / 10) || 1;
        setAnimatedScore(current > score ? score : current);
      }
    }, 30);
    return () => clearInterval(interval);
  }, [score]);

  const getZoneColor = (s) => s >= 70 ? '#22c55e' : s > 40 ? '#eab308' : '#ef4444';
  const color = getZoneColor(animatedScore);
  
  const dashArray = 251.2;
  const dashOffset = dashArray - (dashArray * animatedScore) / 100;
  
  let confBadge = "Low";
  let confColor = "var(--danger)";
  if (confidence > 0.8) { confBadge = "High"; confColor = "var(--success)"; }
  else if (confidence > 0.5) { confBadge = "Medium"; confColor = "var(--warning)"; }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width="180" height="180" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" fill="transparent" stroke="#1f2937" strokeWidth="12" />
        <circle 
          cx="50" cy="50" r="40" 
          fill="transparent" 
          stroke={color} 
          strokeWidth="12" 
          strokeDasharray={dashArray} 
          strokeDashoffset={dashOffset} 
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
          style={{ transition: 'stroke-dashoffset 0.1s linear' }}
        />
        <text x="50" y="58" textAnchor="middle" fill="white" fontSize="28" fontWeight="800">
          {animatedScore}
        </text>
      </svg>
      <div style={{ marginTop: 16, textAlign: 'center' }}>
        <div style={{ fontWeight: 600, fontSize: '1.1rem', color: 'var(--text-primary)' }}>Quantum Safety Score</div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6, marginTop: 8 }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Model Confidence:</span>
          <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: 12, background: 'var(--bg-elevated)', color: confColor, border: `1px solid ${confColor}` }}>
            {confBadge} ({(confidence * 100).toFixed(0)}%)
          </span>
        </div>
      </div>
    </div>
  );
}
