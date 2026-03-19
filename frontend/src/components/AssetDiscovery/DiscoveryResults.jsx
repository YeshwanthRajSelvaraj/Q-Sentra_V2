import React from 'react';
import { Check, X, Server, Globe } from 'lucide-react';

export default function DiscoveryResults({ results, onAction }) {
  if (!results || results.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>No recent discovery results.</div>;
  }

  const getSourceIcon = (src) => {
    if (src === 'CT_LOG') return <Globe size={14} style={{ marginRight: 6, color: '#3b82f6' }} />;
    return <Server size={14} style={{ marginRight: 6, color: '#8b5cf6' }} />;
  };

  const getSourceLabel = (src) => {
    if (src === 'CT_LOG') return 'CT Logs';
    if (src === 'DNS') return 'DNS Enum';
    if (src === 'REVERSE') return 'Reverse DNS';
    return src;
  };

  return (
    <div className="card" style={{ marginTop: 24 }}>
      <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between' }}>
        <span className="card-title">Live Discovery Queue</span>
        <span className="badge" style={{ background: 'rgba(59,130,246,0.1)', color: '#3b82f6', padding: '4px 8px', borderRadius: 12, fontSize: '0.75rem', fontWeight: 600 }}>
          {results.filter(r => r.status === 'PENDING').length} Pending Review
        </span>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>First Seen</th>
            <th>Hostname</th>
            <th>IP Address</th>
            <th>Source</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {results.map(r => (
            <tr key={r.id}>
              <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                 {new Date(r.first_seen).toLocaleString()}
              </td>
              <td className="domain" style={{ fontWeight: 600 }}>{r.hostname}</td>
              <td style={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>{r.ip_address || '---'}</td>
              <td>
                <span className="chip" style={{ display: 'flex', alignItems: 'center', width: 'fit-content', background: 'var(--bg-elevated)', border: '1px solid var(--border-color)' }}>
                  {getSourceIcon(r.source)} {getSourceLabel(r.source)}
                </span>
              </td>
              <td>
                <span className={`score-badge ${r.status === 'CONFIRMED' ? 'safe' : r.status === 'IGNORED' ? 'danger' : 'warning'}`}>
                  {r.status}
                </span>
              </td>
              <td>
                {r.status === 'PENDING' ? (
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button 
                      onClick={() => onAction('confirm', r.id)}
                      className="btn hover-effect" 
                      style={{ padding: '6px 10px', background: 'rgba(34,197,94,0.15)', color: '#22c55e', border: '1px solid rgba(34,197,94,0.3)', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: 6, fontWeight: 600 }}
                    >
                      <Check size={14} /> Confirm
                    </button>
                    <button 
                      onClick={() => onAction('ignore', r.id)}
                      className="btn hover-effect" 
                      style={{ padding: '6px 10px', background: 'rgba(239,68,68,0.15)', color: '#ef4444', border: '1px solid rgba(239,68,68,0.3)', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: 6, fontWeight: 600 }}
                    >
                      <X size={14} /> Ignore
                    </button>
                  </div>
                ) : (
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Actioned</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
