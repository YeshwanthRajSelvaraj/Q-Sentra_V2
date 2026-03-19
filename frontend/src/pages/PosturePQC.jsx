import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
import { MOCK_ASSETS, ASSET_STATS, getScoreColor, getScoreClass, getRiskIcon } from '../mockData';
import PQCGauge from '../components/PQC/PQCGauge';
import SHAPExplainer from '../components/PQC/SHAPExplainer';

const PQC_ALGOS = [
  { algo: 'ML-KEM-768', fips: '203', type: 'KEM', adopted: MOCK_ASSETS.filter(a => a.keyExchange === 'ML-KEM-768').length, total: ASSET_STATS.total, level: 'Level 3' },
  { algo: 'ML-KEM-1024', fips: '203', type: 'KEM', adopted: MOCK_ASSETS.filter(a => a.keyExchange === 'ML-KEM-1024').length, total: ASSET_STATS.total, level: 'Level 5' },
  { algo: 'X25519+Kyber768', fips: '203*', type: 'Hybrid KEM', adopted: MOCK_ASSETS.filter(a => a.keyExchange === 'X25519+Kyber768').length, total: ASSET_STATS.total, level: 'Level 3' },
  { algo: 'ML-DSA-65', fips: '204', type: 'Signature', adopted: MOCK_ASSETS.filter(a => a.signatureAlgorithm === 'ML-DSA-65').length, total: ASSET_STATS.total, level: 'Level 3' },
  { algo: 'ML-DSA-87', fips: '204', type: 'Signature', adopted: MOCK_ASSETS.filter(a => a.signatureAlgorithm === 'ML-DSA-87').length, total: ASSET_STATS.total, level: 'Level 5' },
  { algo: 'SLH-DSA-128f', fips: '205', type: 'Hash Signature', adopted: MOCK_ASSETS.filter(a => a.signatureAlgorithm === 'SLH-DSA-128f').length, total: ASSET_STATS.total, level: 'Level 1' },
];

const radarData = [
  { metric: 'TLS 1.3', value: Math.round(ASSET_STATS.tls13 / ASSET_STATS.total * 100) },
  { metric: 'PQC KEX', value: Math.round(MOCK_ASSETS.filter(a => a.keyExchange.includes('ML-KEM') || a.keyExchange.includes('Kyber')).length / ASSET_STATS.total * 100) },
  { metric: 'PQC Sig', value: Math.round(MOCK_ASSETS.filter(a => a.signatureAlgorithm.includes('ML-DSA') || a.signatureAlgorithm.includes('SLH-DSA')).length / ASSET_STATS.total * 100) },
  { metric: 'Strong Keys', value: Math.round(MOCK_ASSETS.filter(a => a.keySize >= 3072 || a.keyExchange.includes('ML-KEM')).length / ASSET_STATS.total * 100) },
  { metric: 'Valid Certs', value: Math.round(MOCK_ASSETS.filter(a => new Date(a.certificate.expiry) > new Date(2026, 2, 19)).length / ASSET_STATS.total * 100) },
  { metric: 'FIPS Compliant', value: Math.round(MOCK_ASSETS.filter(a => a.quantumScore >= 90).length / ASSET_STATS.total * 100) },
];

const scoreBreakdown = MOCK_ASSETS.map(a => ({ name: a.domain.split('.')[0], score: a.quantumScore })).slice(0, 20);

function AssetScoreViewer() {
  const [hostname, setHostname] = useState('api.pnb.co.in');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchScore = async () => {
    if (!hostname) return;
    setLoading(true);
    try {
      const resp = await fetch(`http://127.0.0.1:8000/api/pqc-score/${hostname}`);
      const json = await resp.json();
      setData(json);
    } catch (e) {
      console.error(e);
      setData({
        score: 65,
        confidence: 0.88,
        explanations: [
           { feature: "uses_weak_signature", contribution: -20, desc: "Certificate uses SHA-1 signature (deprecated)" },
           { feature: "tls_1_3", contribution: 15, desc: "Supports TLS 1.3 with strong ciphers" }
        ]
      });
    }
    setLoading(false);
  }

  const batchScore = async () => {
    try {
      await fetch(`http://127.0.0.1:8000/api/pqc-score/batch`);
      alert("Batch scoring initiated in background.");
    } catch (e) {
      console.error(e);
    }
  }

  return (
    <div className="card" style={{ marginBottom: 24 }}>
       <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span className="card-title">AI-Powered Asset Quantum Scoring</span>
          <button className="btn btn-outline" onClick={batchScore} style={{ padding: '4px 12px', fontSize: '0.75rem' }}>🔄 Score All Assets</button>
       </div>
       <div style={{ padding: 20 }}>
         <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
            <input type="text" value={hostname} onChange={e => setHostname(e.target.value)} placeholder="Enter hostname (e.g. api.pnb.co.in)" style={{ flex: 1, padding: '8px 12px', borderRadius: 6, background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', color: 'white', outline: 'none' }} />
            <button className="btn btn-primary" onClick={fetchScore} disabled={loading}>{loading ? 'Analyzing Feature Spaces...' : 'Analyze Posture'}</button>
         </div>
         
         {data && (
           <div style={{ display: 'grid', gridTemplateColumns: 'minmax(250px, 1fr) 2fr', gap: 32, alignItems: 'start' }}>
              <div style={{ padding: 16, background: 'rgba(255,255,255,0.02)', borderRadius: 12, border: '1px solid rgba(255,255,255,0.05)' }}>
                  <PQCGauge score={data.score} confidence={data.confidence} />
              </div>
              <div>
                 <h4 style={{ margin: '0 0 16px 0', fontSize: '1.2rem', color: 'var(--text-primary)' }}>"Why This Score?" — SHAP Analysis</h4>
                 <SHAPExplainer explanations={data.explanations} />
                 
                 <div style={{ marginTop: 24, padding: 16, background: 'rgba(99,102,241,0.1)', borderRadius: 8, borderLeft: '4px solid #6366f1' }}>
                     <h4 style={{ margin: '0 0 12px 0', color: '#818cf8' }}>Remediation Recommendations</h4>
                     <ul style={{ paddingLeft: 20, margin: 0, color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
                        {data.score < 75 && <li>Update certificate signature to SHA-256 or a quantum-safe signature like ML-DSA-65.</li>}
                        {data.score < 90 && <li>Replace RSA-2048 with ECDHE or PQC KEM Kyber-768/ML-KEM for key exchange.</li>}
                        <li>Ensure TLS 1.3 is exclusively enabled; disable all legacy protocols (TLS 1.2 and below).</li>
                     </ul>
                 </div>
              </div>
           </div>
         )}
       </div>
    </div>
  )
}

export default function PosturePQC() {
  const pqcReady = MOCK_ASSETS.filter(a => a.quantumScore >= 90).length;
  const transitioning = MOCK_ASSETS.filter(a => a.quantumScore >= 60 && a.quantumScore < 90).length;
  const atRisk = MOCK_ASSETS.filter(a => a.quantumScore < 60).length;

  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div><h1 className="page-title">Posture of PQC</h1><p className="page-subtitle">Post-Quantum Cryptography readiness assessment across all assets</p></div>
      </div>

      <AssetScoreViewer />

      {/* Summary Cards */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: 24 }}>
        <div className="kpi-card accent-safe"><div className="kpi-value" style={{ color: '#22c55e' }}>{pqcReady}</div><div className="kpi-label">🟢 PQC Ready (Score ≥90)</div></div>
        <div className="kpi-card accent-primary"><div className="kpi-value" style={{ color: '#eab308' }}>{transitioning}</div><div className="kpi-label">🟡 Transitioning (60-89)</div></div>
        <div className="kpi-card accent-danger"><div className="kpi-value" style={{ color: '#f97316' }}>{atRisk}</div><div className="kpi-label">🟠🔴 At Risk (&lt;60)</div></div>
        <div className="kpi-card accent-quantum"><div className="kpi-value">{ASSET_STATS.avgScore}</div><div className="kpi-label">Average Quantum Score</div></div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 16, marginBottom: 20 }}>
        {/* Algorithm Adoption */}
        <div className="card">
          <div className="card-header"><span className="card-title">NIST PQC Algorithm Adoption</span></div>
          <table className="data-table">
            <thead><tr><th>Algorithm</th><th>FIPS</th><th>Type</th><th>Security Level</th><th>Adopted</th><th>Coverage</th></tr></thead>
            <tbody>
              {PQC_ALGOS.map((a, i) => {
                const pct = Math.round(a.adopted / a.total * 100);
                return (
                  <tr key={i}>
                    <td style={{ fontWeight: 600, color: '#22c55e' }}>{a.algo}</td>
                    <td><span className="chip tls13">FIPS {a.fips}</span></td>
                    <td style={{ fontSize: '0.78rem' }}>{a.type}</td>
                    <td style={{ fontSize: '0.78rem' }}>{a.level}</td>
                    <td><span style={{ fontWeight: 600 }}>{a.adopted}</span><span style={{ color: 'var(--text-muted)' }}>/{a.total}</span></td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <div style={{ width: 60, height: 6, background: 'var(--bg-elevated)', borderRadius: 3, overflow: 'hidden' }}>
                          <div style={{ width: `${pct}%`, height: '100%', background: pct > 10 ? '#22c55e' : '#ef4444', borderRadius: 3 }} />
                        </div>
                        <span style={{ fontSize: '0.75rem', fontWeight: 600, color: pct > 10 ? '#22c55e' : '#ef4444' }}>{pct}%</span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Radar Chart */}
        <div className="card">
          <div className="card-header"><span className="card-title">PQC Readiness Radar</span></div>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(99,102,241,0.15)" />
              <PolarAngleAxis dataKey="metric" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <PolarRadiusAxis domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 10 }} />
              <Radar name="Coverage" dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.2} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Per-Asset Scores */}
      <div className="card">
        <div className="card-header"><span className="card-title">Per-Asset Quantum Score (Top 20)</span><span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Target: 90+</span></div>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={scoreBreakdown} barCategoryGap="12%">
            <XAxis dataKey="name" stroke="#64748b" fontSize={9} tickLine={false} axisLine={false} angle={-45} textAnchor="end" height={60} />
            <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} domain={[0, 100]} />
            <Tooltip contentStyle={{ background: '#141b2d', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, fontSize: 11 }} />
            <Bar dataKey="score" radius={[3, 3, 0, 0]}>{scoreBreakdown.map((e, i) => <Cell key={i} fill={getScoreColor(e.score)} />)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
