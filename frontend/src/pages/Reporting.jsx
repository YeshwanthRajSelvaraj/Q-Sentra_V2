import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, LineChart, Line, PieChart, Pie } from 'recharts';
import { MOCK_ASSETS, ASSET_STATS, MOCK_ACTIVITY, getScoreColor, getScoreClass } from '../mockData';
import { dashboardService } from '../services/dashboardService';

const REPORT_TYPES = [
  { name: 'Executive Summary', desc: 'High-level PQC readiness for CXO/Board', format: 'PDF', icon: '📊' },
  { name: 'CBOM Report', desc: 'CycloneDX 1.6 cryptographic bill of materials', format: 'JSON/XML', icon: '📋' },
  { name: 'Compliance Audit', desc: 'RBI, PCI-DSS, ISO 27001 compliance evidence', format: 'PDF', icon: '✅' },
  { name: 'Risk Assessment', desc: 'HNDL threat analysis and blast radius report', format: 'PDF', icon: '⚠️' },
  { name: 'Remediation Progress', desc: '9-month migration roadmap status update', format: 'PDF', icon: '🔧' },
  { name: 'Quantum Certificate Ledger', desc: 'Blockchain-anchored certificate registry', format: 'PDF/JSON', icon: '🏆' },
];

const TREND_DATA = [
  { week: 'W1', assets: 95, score: 28, scans: 5 },
  { week: 'W2', assets: 102, score: 30, scans: 8 },
  { week: 'W3', assets: 110, score: 32, scans: 12 },
  { week: 'W4', assets: 118, score: 35, scans: 15 },
  { week: 'W5', assets: 124, score: 38, scans: 18 },
  { week: 'W6', assets: 128, score: ASSET_STATS.avgScore, scans: 22 },
];

const ownerDist = (() => {
  const m = {};
  MOCK_ASSETS.forEach(a => { m[a.owner] = (m[a.owner] || 0) + 1; });
  return Object.entries(m).sort((a, b) => b[1] - a[1]).map(([name, count]) => ({ name, count }));
})();

export default function Reporting() {
  const [generating, setGenerating] = useState(null);
  const [activities, setActivities] = useState(MOCK_ACTIVITY);

  useEffect(() => {
    dashboardService.getRecentActivity().then(act => {
      if (act && act.length > 0) setActivities(act);
    });
  }, []);

  const generate = async (name) => {
    setGenerating(name);
    // Simulate generation or hit real endpoint if exists
    setTimeout(() => {
      setGenerating(null);
      alert(`${name} report generated successfully.`);
    }, 2000);
  };


  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div><h1 className="page-title">Reporting</h1><p className="page-subtitle">Automated compliance reporting and analytics dashboard</p></div>
        <button className="btn btn-primary" onClick={() => generate('all')}>📄 Generate All Reports</button>
      </div>

      {/* Report Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        {REPORT_TYPES.map(r => (
          <div className="card" key={r.name} style={{ cursor: 'pointer' }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12, marginBottom: 12 }}>
              <span style={{ fontSize: '1.8rem' }}>{r.icon}</span>
              <div>
                <h3 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: 4 }}>{r.name}</h3>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{r.desc}</p>
              </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="chip tls13">{r.format}</span>
              <button className="btn btn-outline" style={{ fontSize: '0.72rem', padding: '4px 12px' }}
                onClick={() => generate(r.name)} disabled={generating === r.name}>
                {generating === r.name ? '⏳ Generating...' : '📥 Download'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Analytics */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 20 }}>
        <div className="card">
          <div className="card-header"><span className="card-title">Weekly Progress Trend</span></div>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={TREND_DATA}>
              <XAxis dataKey="week" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }} />
              <Line type="monotone" dataKey="assets" stroke="#6366f1" strokeWidth={2} name="Assets" dot={{ r: 3 }} />
              <Line type="monotone" dataKey="score" stroke="#22c55e" strokeWidth={2} name="Avg Score" dot={{ r: 3 }} />
              <Line type="monotone" dataKey="scans" stroke="#06b6d4" strokeWidth={2} name="Scans" dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="card-header"><span className="card-title">Assets by Owner</span></div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={ownerDist} barCategoryGap="15%">
              <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }} />
              <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Scan History */}
      <div className="card">
        <div className="card-header"><span className="card-title">Scan History Log</span></div>
        {activities.map(a => (
          <div key={a.id} className="compliance-row">
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, flex: 1 }}>
              <div className={`activity-dot ${a.severity}`} />
              <span style={{ fontSize: '0.82rem' }}>{a.message || a.description}</span>
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{a.time || new Date(a.created_at).toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
