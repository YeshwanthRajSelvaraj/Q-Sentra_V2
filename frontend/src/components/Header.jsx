import React from 'react';
import { Bell, Search, LogOut, Wifi } from 'lucide-react';

const TITLES = {
  dashboard: 'Home', assets: 'Asset Inventory', discovery: 'Asset Discovery',
  cbom: 'Cryptographic Bill of Materials', posture: 'Posture of PQC',
  'blast-radius': 'Blast Radius Visualizer', 'cyber-rating': 'Cyber Rating',
  remediation: 'Remediation Hub', certificates: 'Certificate Registry',
  compliance: 'Compliance Dashboard', reporting: 'Reporting',
};

export default function Header({ currentPage, onLogout }) {
  return (
    <header className="header">
      <div className="header-left">
        <h2 className="header-title">{TITLES[currentPage] || 'Q-Sentra'}</h2>
      </div>
      <div className="header-right">
        <div className="header-status live"><span className="pulse" /><span>Live Monitoring</span></div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', padding: '4px 10px', background: 'var(--bg-card)', borderRadius: 6, border: '1px solid var(--border-color)' }}>
          19 Mar 2026, 21:25 IST
        </div>
        <button className="header-btn" title="Search"><Search size={15} /></button>
        <button className="header-btn" title="Alerts" style={{ position: 'relative' }}>
          <Bell size={15} />
          <span style={{ position: 'absolute', top: 3, right: 3, width: 8, height: 8, borderRadius: '50%', background: '#ef4444', border: '2px solid var(--bg-glass)' }} />
        </button>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          Welcome User: <strong style={{ color: 'var(--accent-secondary)' }}>hackathon_user</strong>
        </div>
        <button className="header-btn" onClick={onLogout} title="Logout"><LogOut size={15} /></button>
      </div>
    </header>
  );
}
