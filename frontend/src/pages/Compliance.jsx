import React from 'react';
import { CheckCircle, AlertCircle, Clock } from 'lucide-react';

const FRAMEWORKS = [
  { name: 'NIST PQC (FIPS 203/204/205)', status: 'partial', coverage: 10, details: '1/10 assets fully FIPS compliant', icon: '🔬' },
  { name: 'RBI Digital Payment Security', status: 'compliant', coverage: 85, details: 'Encryption controls active, PQC migration in progress', icon: '🏦' },
  { name: 'PCI-DSS v4.0 Requirement 4', status: 'partial', coverage: 60, details: 'TLS 1.3 migration in progress for payment assets', icon: '💳' },
  { name: 'ISO 27001:2022 (A.8.24, A.5.14)', status: 'compliant', coverage: 90, details: 'Cryptographic lifecycle management active, audit trail maintained', icon: '📋' },
  { name: 'GDPR Article 32', status: 'compliant', coverage: 80, details: 'State-of-art encryption measures implemented', icon: '🇪🇺' },
  { name: 'India DPDP Act 2023', status: 'compliant', coverage: 75, details: 'Personal data protection controls active', icon: '🇮🇳' },
];

const statusConfig = {
  compliant: { color: '#22c55e', bg: 'rgba(34,197,94,0.1)', label: 'Compliant', Icon: CheckCircle },
  partial: { color: '#eab308', bg: 'rgba(234,179,8,0.1)', label: 'Partial', Icon: Clock },
  'non-compliant': { color: '#ef4444', bg: 'rgba(239,68,68,0.1)', label: 'Non-Compliant', Icon: AlertCircle },
};

export default function Compliance() {
  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div>
          <h1 className="page-title">Compliance Dashboard</h1>
          <p className="page-subtitle">Regulatory compliance status across RBI, PCI-DSS, ISO 27001, GDPR, and DPDP</p>
        </div>
      </div>

      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: 24 }}>
        <div className="kpi-card accent-safe">
          <div className="kpi-value" style={{ color: '#22c55e' }}>4</div>
          <div className="kpi-label">Frameworks Compliant</div>
        </div>
        <div className="kpi-card accent-primary">
          <div className="kpi-value" style={{ color: '#eab308' }}>2</div>
          <div className="kpi-label">Partially Compliant</div>
        </div>
        <div className="kpi-card accent-quantum">
          <div className="kpi-value">66.7%</div>
          <div className="kpi-label">Overall Compliance Rate</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">Compliance Framework Status</span>
        </div>
        {FRAMEWORKS.map((fw) => {
          const st = statusConfig[fw.status];
          return (
            <div className="compliance-row" key={fw.name}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, flex: 1 }}>
                <span style={{ fontSize: '1.4rem' }}>{fw.icon}</span>
                <div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-primary)' }}>{fw.name}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 2 }}>{fw.details}</div>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <div className="compliance-bar" style={{ width: 140 }}>
                  <div className="fill" style={{ width: `${fw.coverage}%`, background: st.color }} />
                </div>
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: st.color, width: 40, textAlign: 'right' }}>{fw.coverage}%</span>
                <span className="score-badge" style={{ background: st.bg, color: st.color, minWidth: 85, justifyContent: 'center' }}>
                  <st.Icon size={12} /> {st.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-header"><span className="card-title">Audit Trail</span></div>
        {[
          { date: '2026-03-10', action: 'Quarterly PQC compliance assessment completed', user: 'admin', result: 'Partial' },
          { date: '2026-03-01', action: 'Quantum-safe certificate issued for swift.pnb.co.in', user: 'system', result: 'Pass' },
          { date: '2026-02-15', action: 'ISO 27001 internal audit — cryptographic controls review', user: 'auditor01', result: 'Pass' },
          { date: '2026-02-01', action: 'RBI Digital Payment Security self-assessment submitted', user: 'admin', result: 'Pass' },
          { date: '2026-01-15', action: 'PCI-DSS v4.0 Req 4 gap analysis completed', user: 'analyst01', result: 'Gaps Found' },
        ].map((entry, i) => (
          <div key={i} className="compliance-row">
            <div style={{ display: 'flex', gap: 12, flex: 1 }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', width: 80 }}>{entry.date}</span>
              <span style={{ fontSize: '0.85rem' }}>{entry.action}</span>
            </div>
            <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{entry.user}</span>
              <span className={`score-badge ${entry.result === 'Pass' ? 'safe' : entry.result === 'Partial' ? 'moderate' : 'high'}`}>{entry.result}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
