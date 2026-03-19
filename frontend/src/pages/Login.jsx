import React, { useState } from 'react';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      // In demo mode, accept any login
      localStorage.setItem('qsentra_token', 'demo-jwt-token');
      localStorage.setItem('qsentra_user', JSON.stringify({ username: username || 'admin', role: 'admin' }));
      setTimeout(() => { setLoading(false); onLogin(); }, 800);
    } catch (err) {
      setError('Authentication failed');
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-logo">
          <div className="login-logo-icon">Q</div>
          <div>
            <h1>Q-Sentra</h1>
            <p>PNB Quantum Guard</p>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Quantum-Proof Cryptographic Asset Management
          </p>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4 }}>
            Punjab National Bank — Cybersecurity Division
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input className="form-input" type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} autoFocus />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input className="form-input" type="password" placeholder="Enter password" value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          {error && <div style={{ color: '#ef4444', fontSize: '0.82rem', marginBottom: 12 }}>{error}</div>}
          <button className="btn-login" type="submit" disabled={loading}>
            {loading ? '🔐 Authenticating...' : '🛡️ Secure Login'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: 24 }}>
          <div style={{ display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap' }}>
            {['MFA Enabled', 'TLS 1.3', 'AES-256'].map(tag => (
              <span key={tag} style={{ fontSize: '0.65rem', padding: '3px 8px', borderRadius: 12, background: 'var(--accent-glow)', color: 'var(--accent-secondary)', fontWeight: 500 }}>{tag}</span>
            ))}
          </div>
          <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 16 }}>
            Protected by quantum-safe authentication protocols
          </p>
        </div>
      </div>
    </div>
  );
}
