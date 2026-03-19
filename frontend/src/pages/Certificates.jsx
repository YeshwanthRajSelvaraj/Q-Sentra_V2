import React from 'react';
import { Shield, ExternalLink, Copy, CheckCircle } from 'lucide-react';
import { MOCK_CERTS, getScoreColor, getScoreClass } from '../mockData';

export default function Certificates() {
  return (
    <div className="fade-in">
      <div className="page-title-bar">
        <div>
          <h1 className="page-title">Certificate Registry</h1>
          <p className="page-subtitle">Quantum-safe certificates with blockchain-anchored verification</p>
        </div>
        <button className="btn btn-primary"><Shield size={14} /> Issue Certificate</button>
      </div>

      <div className="cert-grid">
        {MOCK_CERTS.map(cert => (
          <div className="cert-card" key={cert.certId}>
            <div className="cert-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div className="cert-shield"><Shield size={22} /></div>
                <div className="cert-info">
                  <h3>{cert.assetId}</h3>
                  <p>{cert.certId}</p>
                </div>
              </div>
              <span className={`score-badge ${getScoreClass(cert.quantumScore)}`}>Score: {cert.quantumScore}</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 0, marginBottom: 16 }}>
              <div className="cert-detail-row"><span className="label">Algorithms</span><span className="value">{cert.algorithms.join(', ')}</span></div>
              <div className="cert-detail-row"><span className="label">Issued</span><span className="value">{cert.issuedAt}</span></div>
              <div className="cert-detail-row"><span className="label">Valid Until</span><span className="value">{cert.validUntil}</span></div>
              <div className="cert-detail-row"><span className="label">Status</span><span className="value" style={{ color: '#22c55e' }}>● {cert.status}</span></div>
              <div className="cert-detail-row"><span className="label">Hash</span><span className="value" style={{ fontSize: '0.7rem' }}>{cert.certificateHash}</span></div>
              <div className="cert-detail-row"><span className="label">Blockchain TX</span><span className="value">{cert.blockchainTx}</span></div>
              <div className="cert-detail-row"><span className="label">Block #</span><span className="value">{cert.blockNumber}</span></div>
              <div className="cert-detail-row"><span className="label">Network</span><span className="value">{cert.network}</span></div>
            </div>

            <div style={{ display: 'flex', gap: 8 }}>
              <button className="btn btn-outline" style={{ flex: 1, justifyContent: 'center', fontSize: '0.78rem' }}>
                <ExternalLink size={13} /> Verify on Chain
              </button>
              <button className="btn btn-outline" style={{ flex: 1, justifyContent: 'center', fontSize: '0.78rem' }}>
                <Copy size={13} /> Export PDF
              </button>
            </div>
          </div>
        ))}

        {/* Placeholder for assets pending certification */}
        <div className="cert-card" style={{ opacity: 0.5, borderStyle: 'dashed' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 200, flexDirection: 'column', gap: 12, color: 'var(--text-muted)' }}>
            <Shield size={40} strokeWidth={1} />
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontWeight: 500, marginBottom: 4 }}>Pending Certifications</div>
              <div style={{ fontSize: '0.8rem' }}>8 assets awaiting PQC migration to qualify for quantum-safe certification</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
