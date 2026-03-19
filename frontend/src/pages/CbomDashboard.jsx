import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { MOCK_ASSETS, ASSET_STATS, KEY_LENGTH_STATS, CIPHER_STATS, CA_STATS } from '../mockData';
import CBOMViewer from '../components/CBOM/CBOMViewer';

const TLS_DIST = [
  { name: 'TLS 1.3', value: ASSET_STATS.tls13, color: '#22c55e' },
  { name: 'TLS 1.2', value: ASSET_STATS.tls12, color: '#eab308' },
  { name: 'TLS 1.1', value: ASSET_STATS.tls11, color: '#f97316' },
  { name: 'TLS 1.0', value: ASSET_STATS.tls10, color: '#ef4444' },
];

const weakCrypto = MOCK_ASSETS.filter(a => a.quantumScore < 30).length;
const certIssues = ASSET_STATS.expiringCerts + ASSET_STATS.expiredCerts;

export default function CbomDashboard() {
  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const selectedAsset = queryParams.get('asset');

  if (selectedAsset) {
    return (
      <div className="fade-in">
         <button className="btn btn-outline" onClick={() => navigate('/cbom')} style={{ marginBottom: 16 }}>← Back to CBOM Dashboard</button>
         <CBOMViewer hostname={selectedAsset} />
      </div>
    );
  }

  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div><h1 className="page-title">Cryptographic Bill of Materials</h1><p className="page-subtitle">CycloneDX 1.6 compliant CBOM — comprehensive cryptographic inventory</p></div>
        <div style={{display:'flex',gap:8}}>
          <button className="btn btn-outline">📥 Export JSON</button>
          <button className="btn btn-outline">📥 Export XML</button>
          <button className="btn btn-primary">📄 Generate Report</button>
        </div>
      </div>

      {/* KPI Row */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(5, 1fr)', marginBottom: 24 }}>
        {[
          { label: 'Total Applications', value: ASSET_STATS.total, color: 'var(--accent-secondary)' },
          { label: 'Sites Surveyed', value: Math.round(ASSET_STATS.total * 0.88), color: '#06b6d4' },
          { label: 'Active Certificates', value: Math.round(ASSET_STATS.total * 0.92), color: '#22c55e' },
          { label: 'Weak Cryptography', value: weakCrypto, color: '#ef4444' },
          { label: 'Certificate Issues', value: certIssues, color: '#f97316' },
        ].map((k, i) => (
          <div className="kpi-card" key={i} style={{ borderTop: `3px solid ${k.color}` }}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value" style={{ color: k.color }}>{k.value}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr 1fr', gap: 16, marginBottom: 20 }}>
        {/* Key Length Distribution */}
        <div className="card">
          <div className="card-header"><span className="card-title">Key Length Distribution</span></div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={KEY_LENGTH_STATS} layout="vertical" barCategoryGap="15%">
              <XAxis type="number" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis type="category" dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} width={65} />
              <Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }} />
              <Bar dataKey="count" fill="#6366f1" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Cipher Usage */}
        <div className="card">
          <div className="card-header"><span className="card-title">Cipher Usage</span></div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {CIPHER_STATS.map((c, i) => {
              const pct = Math.round(c.count / ASSET_STATS.total * 100);
              const isWeak = c.fullName.includes('DES') || c.fullName.includes('CBC');
              return (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: '0.7rem', flex: 1, color: isWeak ? '#ef4444' : 'var(--text-secondary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontFamily: 'monospace' }}>
                    {isWeak && '⚠️ '}{c.name}
                  </span>
                  <div style={{ width: 100, height: 18, background: 'var(--bg-elevated)', borderRadius: 3, overflow: 'hidden', display: 'flex', alignItems: 'center' }}>
                    <div style={{ width: `${pct * 3}%`, height: '100%', background: isWeak ? '#ef4444' : '#6366f1', borderRadius: 3, display: 'flex', alignItems: 'center', justifyContent: 'flex-end', paddingRight: 4 }}>
                      <span style={{ fontSize: '0.6rem', color: 'white', fontWeight: 600 }}>{c.count}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Top CAs + TLS Versions */}
        <div className="card">
          <div className="card-header"><span className="card-title">Top Certificate Authorities</span></div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 16 }}>
            {CA_STATS.slice(0, 5).map((ca, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{ca.name}</span>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-secondary)' }}>{ca.count}</span>
              </div>
            ))}
          </div>
          <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: 12 }}>
            <div className="card-title" style={{ marginBottom: 8 }}>Encryption Protocols</div>
            <ResponsiveContainer width="100%" height={110}>
              <PieChart>
                <Pie data={TLS_DIST} cx="50%" cy="50%" innerRadius={28} outerRadius={45} paddingAngle={3} dataKey="value" stroke="none">
                  {TLS_DIST.map((e, i) => <Cell key={i} fill={e.color} />)}
                </Pie>
                <Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap' }}>
              {TLS_DIST.map((t, i) => <span key={i} style={{ fontSize: '0.65rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 3 }}><span style={{ width: 7, height: 7, borderRadius: 2, background: t.color, display: 'inline-block' }} />{t.name} {t.value}</span>)}
            </div>
          </div>
        </div>
      </div>

      {/* Detailed CBOM Table */}
      <div className="data-table-wrapper">
        <div className="data-table-header"><span className="card-title">Cryptographic Asset Details</span></div>
        <table className="data-table">
          <thead><tr><th>Application</th><th>Key Length</th><th>Cipher</th><th>Certificate Authority</th><th>TLS</th><th>Q-Score</th></tr></thead>
          <tbody>
            {MOCK_ASSETS.slice(0, 12).map(a => (
              <tr key={a.id}>
                <td className="domain">{a.domain}</td>
                <td><span className={`score-badge ${a.keySize >= 3072 ? 'safe' : a.keySize >= 2048 ? 'moderate' : 'critical'}`}>{a.keySize}-bit</span></td>
                <td style={{ fontSize: '0.75rem', fontFamily: 'monospace', maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{a.cipherSuite}</td>
                <td>{a.certificate.issuer}</td>
                <td><span className={`chip ${a.tlsVersion === '1.3' ? 'tls13' : 'tls12'}`}>TLS {a.tlsVersion}</span></td>
                <td style={{ fontWeight: 600, color: a.quantumScore >= 90 ? '#22c55e' : a.quantumScore >= 30 ? '#eab308' : '#ef4444' }}>{a.quantumScore}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
