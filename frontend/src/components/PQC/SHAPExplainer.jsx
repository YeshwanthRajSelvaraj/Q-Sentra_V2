import React from 'react';
import { AlertOctagon, AlertTriangle, CheckCircle, Info } from 'lucide-react';

export default function SHAPExplainer({ explanations }) {
  if (!explanations || explanations.length === 0) {
    return <div style={{ color: 'var(--text-muted)' }}>No explanations available yet.</div>;
  }

  return (
    <div className="shap-explainer">
      {explanations.map((exp, idx) => {
        let Icon = Info;
        let color = '#3b82f6';
        let sentiment = 'Neutral';
        
        if (exp.contribution <= -30) {
          Icon = AlertOctagon;
          color = '#ef4444';
          sentiment = 'Critical Vulnerability';
        } else if (exp.contribution < 0) {
          Icon = AlertTriangle;
          color = '#f97316';
          sentiment = 'Risk Factor';
        } else if (exp.contribution > 0) {
          Icon = CheckCircle;
          color = '#22c55e';
          sentiment = 'Positive Indicator';
        }

        return (
          <div key={idx} style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: 16,
            padding: 16,
            borderRadius: 8,
            background: 'var(--bg-elevated)',
            marginBottom: 12,
            borderLeft: `4px solid ${color}`
          }}>
            <Icon size={24} style={{ color, marginTop: 2 }} />
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                <span style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.95rem' }}>{sentiment}</span>
                <span style={{ 
                  fontSize: '0.75rem', 
                  padding: '2px 8px', 
                  background: 'rgba(255,255,255,0.05)', 
                  borderRadius: 12,
                  color: 'var(--text-muted)'
                }}>
                  Score Impact: <span style={{ color, fontWeight: 700 }}>{exp.contribution > 0 ? '+' : ''}{exp.contribution.toFixed(1)}</span> pts
                </span>
              </div>
              <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {exp.desc}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
